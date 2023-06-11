# Copyright 2023 kazuh
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import tkinter as tk
from tkinter import END, LEFT, ttk
from tkinter.scrolledtext import ScrolledText

from chat.create_chat import get_response, init_log, EXTRA_LOG_FILE_NAME


class ChatGUI:
    def __init__(self):
        init_log(EXTRA_LOG_FILE_NAME)

        self.root = tk.Tk()
        self.root.title("RootTitle")

        self.frame_history = tk.Frame(self.root, height=100)
        self.frame_input_form = tk.Frame(self.root, height=30)
        self.frame_history.pack() #side=LEFT)
        self.frame_input_form.pack()
        # self.frame_history.grid(row=0, column=0, rowspan=2)
        # self.framc_input_form.grid(row=0, column=0, rowspan=2)
        
        self.chatlog = tk.Listbox(self.frame_history, height=25, width=100)
        self.chatlog.pack(side="left", fill="y")

        self.scrollbar = tk.Scrollbar(self.frame_history,  orient="vertical")
        self.scrollbar.config(command=self.chatlog.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.chatlog.config(yscrollcommand=self.scrollbar.set)


        # text_input = tk.StringVar()
        self.text_input = ScrolledText(self.frame_input_form)
        # entry_input = ttk.Entry(root, textvariable=text_input)
        self.button_input = ttk.Button(self.frame_input_form, text="Input", command=lambda: self.get_text())
        self.button_quit = ttk.Button(self.frame_input_form, text="Quit", command=quit)

        self.text_input.bind("<Key>", self.on_key_press)
        # self.text_input.grid(row=0)
        # self.button_input.grid(row=1, column=0)
        # self.button_quit.grid(row=1, column=1)
        self.text_input.pack()
        self.button_input.pack(side=LEFT)
        self.button_quit.pack()

    def add_to_chatlog(self, text):
        self.chatlog.insert(tk.END, text)


    def on_key_press(self, event):
        if event.keysym == 'b' and event.state & 0x4:
            self.get_text()

    def get_text(self):
        content = self.text_input.get(1.0, END)
        print("Input:\n", content)
        response = get_response(content)
        print("ChatGPT:", response)
        self.add_to_chatlog(f"ChatGPT:{response}")


    def start(self):
        self.root.mainloop()

chat_ui = ChatGUI()
chat_ui.add_to_chatlog("Welcome to the chat!")
chat_ui.start()