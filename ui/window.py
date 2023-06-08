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
from tkinter import END, ttk
from tkinter.scrolledtext import ScrolledText

# sys.path.append("")
# 実行中のスクリプトのディレクトリパスを取得
script_directory = os.path.dirname(os.path.abspath(__file__))

# モジュールの相対パスを指定する場合、スクリプトのディレクトリを基準にする
module_path = os.path.join(script_directory, "..", "chat")
sys.path.append(module_path)

# from chat.create_chat import main


def get_text():
    content = text_input.get(1.0, END)
    print("Input:\n", content)
    # main(content)


root = tk.Tk()
root.title("RootTitle")

# text_input = tk.StringVar()
text_input = ScrolledText(root)
# entry_input = ttk.Entry(root, textvariable=text_input)
button_input = ttk.Button(root, text="Input", command=lambda: get_text())
button_quit = ttk.Button(root, text="Quit", command=quit)

text_input.grid(row=0)
button_input.grid(row=1, column=0)
button_quit.grid(row=1, column=1)

root.mainloop()
