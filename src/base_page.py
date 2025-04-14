import tkinter as tk
class BasePage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

    def create_label(self, text, **grid_options):
        label = tk.Label(self, text=text)
        label.grid(**grid_options)
        return label

    def create_entry(self, **grid_options):
        entry = tk.Entry(self)
        entry.grid(**grid_options)
        return entry

    def create_button(self, text, command, **grid_options):
        button = tk.Button(self, text=text, command=command)
        button.grid(**grid_options)
        return button

    def create_option_menu(self, variable, options, **grid_options):
        option_menu = tk.OptionMenu(self, variable, *options)
        option_menu.grid(**grid_options)
        return option_menu