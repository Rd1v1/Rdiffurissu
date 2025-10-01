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
            ("C", self.on_clear_all),
            ("⌫", self.on_backspace),
            ("±", self.on_toggle_sign),
        ])
        set_row_weight(row); row += 1

        # ^ sqrt sin cos
        self._add_row(container, row, [
            ("^",  lambda: self.on_operator("^")),
            ("sqrt", lambda: self.on_unary("sqrt")),
            ("sin", lambda: self.on_unary("sin")),  # в логике sin/cos — в градусах
            ("cos", lambda: self.on_unary("cos")),
        ])
        set_row_weight(row); row += 1

        # floor ceil % /
        self._add_row(container, row, [
            ("floor", None),
            ("ceil", None),
            ("%", lambda: self.on_operator("%")),
            ("/", lambda: self.on_operator("/")),
        ])
        set_row_weight(row); row += 1

        # 7 8 9 *
        self._add_row(container, row, [
            ("7", lambda: self.on_digit("7")),
            ("8", lambda: self.on_digit("8")),
            ("9", lambda: self.on_digit("9")),
            ("*", lambda: self.on_operator("*")),
        ])
        set_row_weight(row); row += 1

        # 4 5 6 -
        self._add_row(container, row, [
            ("4", lambda: self.on_digit("4")),
            ("5", lambda: self.on_digit("5")),
            ("6", lambda: self.on_digit("6")),
            ("-", lambda: self.on_operator("-")),
        ])
        set_row_weight(row); row += 1

        # 1 2 3 +
        self._add_row(container, row, [
            ("1", lambda: self.on_digit("1")),
            ("2", lambda: self.on_digit("2")),
            ("3", lambda: self.on_digit("3")),
            ("+", lambda: self.on_operator("+")),
        ])
        set_row_weight(row); row += 1

        # 0 . [пусто] =
        # Для пустой ячейки ставится Label, чтобы сохранялось равномерное изменений размеров кнопки
        empty = ttk.Label(container, text="")
        defs = [
            ("0", lambda: self.on_digit("0")),
            (".", self.on_dot),
            (empty, None),  # placeholder
            ("=", self.on_equals),
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

        # Применение стилей кнопок
        for child in container.winfo_children():
            if isinstance(child, ttk.Button):
                child.configure(style="Calc.TButton")

        # Минимальный размер окна
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

    # Обработчики событий нажатий на кнопки
    # C
    def on_clear_all(self):
        self.calc.clear_all()
        self.var.set(self.calc.display_value)

    # Цифры
    def on_digit(self, d):
        self.calc.input_digit(d)
        self.var.set(self.calc.display_value)

    # Точка десятичной дроби
    def on_dot(self):
        self.calc.input_dot()
        self.var.set(self.calc.display_value)

    # Смена знака
    def on_toggle_sign(self):
        self.calc.toggle_sign()
        self.var.set(self.calc.display_value)

    # Удаление цифр
    def on_backspace(self):
        self.calc.backspace()
        self.var.set(self.calc.display_value)

    def on_operator(self, op):
        self.calc.set_operator(op)
        self.var.set(self.calc.display_value)

    def on_equals(self):
        self.calc.equals()
        self.var.set(self.calc.display_value)

    def on_unary(self, kind):
        self.calc.apply_unary(kind)
        self.var.set(self.calc.display_value)

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
