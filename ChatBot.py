import tkinter as tk
from tkinter import scrolledtext, Listbox
import json
import re
import random
from PIL import Image, ImageTk 

class IntentClassifier:
    def __init__(self, ):
        intents_file = "J:\\Dhatchan Aca Hackathon\\Team-13\\data.json"
        with open(intents_file, 'r') as file:
            self.intents = json.load(file)
        self.all_patterns = []
        for intent in self.intents.values():
            self.all_patterns.extend(intent['patterns'])

    def classify(self, user_input):
        user_input = user_input.lower()
        scores = {}

        for intent, data in self.intents.items():
            score = 0
            for pattern in data['patterns']:
                if re.search(pattern.lower(), user_input):
                    score += 1
            scores[intent] = score

        classified_intent = max(scores, key=scores.get)
        
        if scores[classified_intent] == 0:
            return 'unknown'
        
        return classified_intent

    def get_suggestions(self, partial_input):
        partial_input = partial_input.lower()
        return [pattern for pattern in self.all_patterns if partial_input in pattern.lower()]

class ChatbotGUI:
    def __init__(self, master, intent_classifier):
        self.master = master
        master.title("Training institute Chatbot")
        # self.geometry("500x500")
        
        self.intent_classifier = intent_classifier
        
        self.chat_display = scrolledtext.ScrolledText(master, state='disabled', height=20)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        # self.chat_display.vbar.configure(troughcolor = 'red', bg = 'red')
        
        send_icon = Image.open("J:\\Dhatchan Aca Hackathon\\Train\\send.png")  
        send_icon = send_icon.resize((30, 30), Image.LANCZOS)  
        self.send_icon = ImageTk.PhotoImage(send_icon)

        
        self.send_button = tk.Button(self.master, image=self.send_icon, command=self.send_message,bd=0)
        self.send_button.grid(row=1,column=1, padx=0, pady=10)

        self.msg_entry = tk.Entry(master,width=80)
        self.msg_entry.grid(row=1, column=0, padx=0.001, pady=10)
        self.msg_entry.bind('<KeyRelease>', self.update_suggestions)
        
        
        
        self.suggestions_list = Listbox(master,fg="#86AB89", height=5,width=80)
        self.suggestions_list.grid(row=2, column=0, padx=0, pady=5)
        self.suggestions_list.bind('<<ListboxSelect>>', self.use_suggestion)
        
        self.master.bind('<Return>', self.send_message)

    def update_suggestions(self, event):
        current_input = self.msg_entry.get()
        suggestions = self.intent_classifier.get_suggestions(current_input)
        
        self.suggestions_list.delete(0, tk.END)
        for suggestion in suggestions[:5]:  
            self.suggestions_list.insert(tk.END, suggestion)

    def use_suggestion(self, event):
        if self.suggestions_list.curselection():
            selected = self.suggestions_list.get(self.suggestions_list.curselection())
            self.msg_entry.delete(0, tk.END)
            self.msg_entry.insert(0, selected)

    def send_message(self, event=None):
        user_message = self.msg_entry.get()
        self.display_message("You: " + user_message)
        
        intent = self.intent_classifier.classify(user_message)
        bot_response = self.get_bot_response(intent)
        self.display_message("Bot: " + bot_response)
        
        self.msg_entry.delete(0, tk.END)
        self.suggestions_list.delete(0, tk.END)

    def display_message(self, message):
        self.chat_display.configure(state='normal',fg='#000000')
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)

    def get_bot_response(self, intent):
        responses = self.intent_classifier.intents[intent]['responses']
        return random.choice(responses)


intent_classifier = IntentClassifier()
root = tk.Tk()
root.geometry("681x500")
root.resizable(False,False)
root.configure(bg='#D1E9F6')
chatbot_gui = ChatbotGUI(root, intent_classifier)
root.mainloop()