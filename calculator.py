import tkinter as tk
from tkinter import ttk
from functions import Calculator

class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Калькулятор")
        self.resizable(True, True)

        self.calc = Calculator()
        self.var = tk.StringVar(value=self.calc.display_value)

        self._build_ui()
        
    def _build_ui(self):
        style = ttk.Style(self)
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")

        style.configure("Calc.TButton", font=("Segoe UI", 14), padding=(10, 8))
        style.configure("Calc.TEntry", padding=6)
        display_font = ("Consolas", 24)

        container = ttk.Frame(self, padding=10)
        container.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Сетка 4xN для кнопок
        for c in range(4):
            container.columnconfigure(c, weight=1, uniform="cols")

        def set_row_weight(row_idx):
            container.rowconfigure(row_idx, weight=1, uniform="rows")

        # Размещение контейнера на форме
        entry = ttk.Entry(container, textvariable=self.var, justify="right")
        entry.configure(font=display_font)
        entry.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0, 10))
        set_row_weight(0)

        row = 1

        # MC MR M+ M-
        self._add_row(container, row, [
            ("MC", None),
            ("MR", None),
            ("M+", None),
            ("M-", None),
        ])
        set_row_weight(row); row += 1

        # CE C ⌫ ±
        self._add_row(container, row, [
            ("CE", None),
            ("C", None),
            ("⌫", None),
            ("±", None),
        ])
        set_row_weight(row); row += 1

        # ^ sqrt sin cos
        self._add_row(container, row, [
            ("^", None),
            ("sqrt", None),
            ("sin", None),
            ("cos", None),
        ])
        set_row_weight(row); row += 1

        # floor ceil % /
        self._add_row(container, row, [
            ("floor", None),
            ("ceil", None),
            ("%", None),
            ("/", None),
        ])
        set_row_weight(row); row += 1

        # 7 8 9 *
        self._add_row(container, row, [
            ("7", None),
            ("8", None),
            ("9", None),
            ("*", None),
        ])
        set_row_weight(row); row += 1

        # 4 5 6 -
        self._add_row(container, row, [
            ("4", None),
            ("5", None),
            ("6", None),
            ("-", None),
        ])
        set_row_weight(row); row += 1

        # 1 2 3 +
        self._add_row(container, row, [
            ("1", None),
            ("2", None),
            ("3", None),
            ("+", None),
        ])
        set_row_weight(row); row += 1

        # 0 . [пусто] =
        # Для пустой ячейки поставим пустой Label, чтобы сохранялось равномерное растяжение
        empty = ttk.Label(container, text="")
        defs = [
            ("0", None),
            (".", None),
            (empty, None),  # placeholder
            ("=", None),
        ]
        col = 0
        for item, cmd in defs:
            if isinstance(item, str):
                btn = ttk.Button(container, text=item, command=cmd, style="Calc.TButton")
                btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
            else:
                # placeholder label
                item.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
            col += 1
        set_row_weight(row)

        # Увеличенные кнопки через стиль
        # Применим стиль ко всем кнопкам
        for child in container.winfo_children():
            if isinstance(child, ttk.Button):
                child.configure(style="Calc.TButton")

        # Минимальный размер окна для удобного старта
        self.update_idletasks()
        self.minsize(350, 520)
        self.geometry("350x520")

    def _add_row(self, parent, row, defs):
        # defs: список из 4 элементов (текст, команда)
        col = 0
        for text, cmd in defs:
            btn = ttk.Button(parent, text=text, command=cmd, style="Calc.TButton")
            btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
            col += 1


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
