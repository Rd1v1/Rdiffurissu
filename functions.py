class Calculator:
    def __init__(self):
        self.clear_all()

    # Полный сброс калькулятора
    def clear_all(self):
        self.display_value = "0"
        self._memory = 0.0
        self._pending_operator = None  # Операторы '+', '-', '*', '/', '%', '^'
        self._stored_operand = None
        self._reset_display = False
        self._error = False

    # Отслеживание ввода чисел
    def input_digit(self, d: str):
        if self._error:
            self.display_value = "0"
            self._error = False
        if self._reset_display:
            self.display_value = d
            self._reset_display = False
            return
        if self.display_value == "0":
            self.display_value = d
        else:
            self.display_value += d

    # Отслеживание ввода точки
    def input_dot(self):
        if self._error:
            self.display_value = "0"
            self._error = False
        if self._reset_display:
            self.display_value = "0."
            self._reset_display = False
            return
        if "." not in self.display_value:
            self.display_value += "."

    # Отслеживание смены знака
    def toggle_sign(self):
        if self._error:
            return
        if self.display_value.startswith("-"):
            self.display_value = self.display_value[1:]
        else:
            if self.display_value != "0":
                self.display_value = "-" + self.display_value

    # Отслеживание удаления символов
    def backspace(self):
        if self._error or self._reset_display:
            self.display_value = "0"
            self._reset_display = False
            self._error = False
            return
        s = self.display_value
        if len(s) > 1:
            s = s[:-1]
        else:
            s = "0"
        self.display_value = s
