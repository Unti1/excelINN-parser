import tkinter as tk
from tkinter import filedialog
import pandas as pd
from multiprocessing import Process
from tools import *
from settings import *

class GUI:
    def __init__(self):
        self.current_position = 0
        self.total_count = 0

    def start_parsing(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        pars = Pars(file_path, True)
        pars.start()
        self.update_labels(pars)

    def update_labels(self, pars):
        self.position_value_label.config(text=str(pars.count_now))
        self.total_count_value_label.config(text=str(pars.max_count))
        self.root.after(100, self.update_labels, pars)  # Периодически обновляем метки каждые 100 миллисекунд

    def run(self):
        self.root = tk.Tk() 

        file_label = tk.Label(self.root, text="Укажите файл Excel:")
        file_label.pack()

        parse_button = tk.Button(self.root, text="Начать парсинг", command=self.start_parsing)
        parse_button.pack()

        position_label = tk.Label(self.root, text="Текущая позиция:")
        position_label.pack()

        self.position_value_label = tk.Label(self.root, text=str(self.current_position))
        self.position_value_label.pack()

        total_count_label = tk.Label(self.root, text="Общее количество:")
        total_count_label.pack()

        self.total_count_value_label = tk.Label(self.root, text=str(self.total_count))
        self.total_count_value_label.pack()

        self.root.mainloop()

if __name__ == "__main__":
    g = GUI()
    g.run()
