class Calculator:
    def __init__(self):
        self.clear_all()

    def clear_all(self):
        self.display_value = "0"
        self._memory = 0.0
        self._pending_operator = None  # '+', '-', '*', '/', '%', '^'
        self._stored_operand = None
        self._reset_display = False
        self._error = False
