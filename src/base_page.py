import tkinter as tk
class BasePage(tk.Frame):
    """A base page with helper methods to reduce redundancy."""
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

    def create_label(self, text, row, column, colspan=None,
                     sticky=None, font=MEDIUM_FONT, width=None, relief=None,
                     padx=None, pady=None, bg=None, fg=None):
        label = tk.Label(self, text=text, width=width, font=font, bg=bg, fg=fg, relief=relief)
        label.grid(row=row, column=column, columnspan=colspan, sticky=sticky, padx=padx, pady=pady)
        return label

    def create_entry(self, row, column, colspan=None, width=FORM_FIELD_WIDTH, padx=5, pady=5, sticky="w", show=None):
        entry = tk.Entry(self, width=width, show=show)
        entry.grid(row=row, column=column, columnspan=colspan, padx=padx, pady=pady, sticky=sticky)
        return entry

    def create_button(self, text, command, row, column, font=MEDIUM_FONT, colspan=None, sticky=None
                      ,relief=None, bg=None, fg=None):
        button = tk.Button(self, text=text, command=command, font=font, relief=relief, bg=bg, fg=fg)
        button.grid(row=row, column=column, columnspan=colspan, sticky=sticky, padx=5, pady=5)
        return button

    def create_optionmenu(self, variable, options, row, column, sticky=None, colspan=None):
        optionmenu = tk.OptionMenu(self, variable, *options)
        optionmenu.grid(row=row, column=column, sticky=sticky, padx=5, pady=5, columnspan=colspan)
        return optionmenu

    def create_radiobutton(self, text, variable, value, row, column, sticky="w", colspan=None, font=MEDIUM_FONT):
        radiobutton = tk.Radiobutton(self, text=text, variable=variable, value=value, font=font)
        radiobutton.grid(row=row, column=column, sticky=sticky, padx=5, pady=5, columnspan=colspan)
        return radiobutton

    def make_grid_responsive(self):
        """Apply weight=1 to all rows and columns that have widgets, making the grid responsive."""
        total_columns, total_rows = self.grid_size()
        for row in range(total_rows):
            self.grid_rowconfigure(row, weight=1)
        for col in range(total_columns):
            self.grid_columnconfigure(col, weight=1)