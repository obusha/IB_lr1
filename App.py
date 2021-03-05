import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.btn = tk.Button(self, text="Выбрать файл", command=self.say_hel)

    def choose_file(self):
        return