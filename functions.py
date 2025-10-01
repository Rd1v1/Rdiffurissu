import math

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

    def set_operator(self, op: str):
        # op in ['+','-','*','/','%','^']
        if self._error:
            return
        try:
            current = float(self.display_value)
        except ValueError:
            self._set_error()
            return

        # Если уже есть оператор — сначала вычислим
        if self._pending_operator is not None and self._stored_operand is not None and not self._reset_display:
            # Выполнить цепочное вычисление
            self._binary_compute(self._pending_operator, self._stored_operand, current)
            if self._error:
                return
            try:
                current = float(self.display_value)
            except Exception:
                self._set_error()
                return

        self._stored_operand = current
        self._pending_operator = op
        self._reset_display = True

    def equals(self):
        if self._error:
            return
        if self._pending_operator is None or self._stored_operand is None:
            return
        try:
            current = float(self.display_value)
        except ValueError:
            self._set_error()
            return
        self._binary_compute(self._pending_operator, self._stored_operand, current)
        # После равно сбрасываем оператор, но оставим результат для продолжения
        self._pending_operator = None
        self._stored_operand = None
        self._reset_display = True

    def apply_unary(self, kind: str):
        # kind in ['sin','cos','sqrt','floor','ceil']
        if self._error:
            return
        try:
            x = float(self.display_value)
            if kind == "sin":
                # sin в градусах
                res = math.sin(math.radians(x))
            elif kind == "cos":
                # cos в градусах
                res = math.cos(math.radians(x))
            else:
                raise ValueError("unknown unary")
            self.display_value = self._fmt(res)
            self._reset_display = True
        except Exception:
            self._set_error() 

    # Внутренние вспомогательные
    def _binary_compute(self, op, a, b):
        try:
            if op == "+":
                res = a + b
            elif op == "-":
                res = a - b
            elif op == "*":
                res = a * b
            elif op == "/":
                if b == 0:
                    raise ZeroDivisionError
                res = a / b
            elif op == "%":
                if b == 0:
                    raise ZeroDivisionError
                res = a % b
            else:
                raise ValueError("unknown operator")
            self.display_value = self._fmt(res)
            self._reset_display = True
        except Exception:
            self._set_error()

    def _fmt(self, x):
        # Удобное форматирование числа
        # Ограничим длину и уберем лишние нули
        try:
            if isinstance(x, float) and (math.isinf(x) or math.isnan(x)):
                return "Error"
            s = f"{x:.12g}"  # до 12 значащих
            return s
        except Exception:
            return str(x)

    def _set_error(self):
        self.display_value = "Error"
        self._error = True
        self._pending_operator = None
        self._stored_operand = None
        self._reset_display = True