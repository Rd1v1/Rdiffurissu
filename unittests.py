import unittest
import math
from functions import Calculator

class TestCalculator(unittest.TestCase):

    def setUp(self):
        """Подготовка чистого калькулятора перед каждым тестом"""
        self.calc = Calculator()

    # Тесты инициализации и сброса
    def test_initial_state(self):
        """Тест начального состояния калькулятора"""
        self.assertEqual(self.calc.display_value, "0")
        self.assertEqual(self.calc._memory, 0.0)
        self.assertIsNone(self.calc._pending_operator)
        self.assertIsNone(self.calc._stored_operand)
        self.assertFalse(self.calc._reset_display)
        self.assertFalse(self.calc._error)

    def test_clear_all(self):
        """Тест полного сброса"""
        # Устанавливаем какое-то состояние
        self.calc.display_value = "123"
        self.calc._memory = 5.0
        self.calc._pending_operator = "+"
        self.calc._stored_operand = 10.0
        self.calc._reset_display = True
        self.calc._error = True
        
        self.calc.clear_all()
        
        self.assertEqual(self.calc.display_value, "0")
        self.assertEqual(self.calc._memory, 0.0)
        self.assertIsNone(self.calc._pending_operator)
        self.assertIsNone(self.calc._stored_operand)
        self.assertFalse(self.calc._reset_display)
        self.assertFalse(self.calc._error)

    def test_clear_entry(self):
        """Тест очистки текущего ввода"""
        self.calc.display_value = "123"
        self.calc._reset_display = True
        self.calc._error = True
        
        self.calc.clear_entry()
        
        self.assertEqual(self.calc.display_value, "0")
        self.assertFalse(self.calc._reset_display)
        self.assertFalse(self.calc._error)

    # Тесты ввода цифр
    def test_input_digit_to_zero(self):
        """Ввод цифры когда на дисплее 0"""
        self.calc.input_digit("5")
        self.assertEqual(self.calc.display_value, "5")

    def test_input_digit_append(self):
        """Добавление цифр к существующему числу"""
        self.calc.display_value = "12"
        self.calc.input_digit("3")
        self.assertEqual(self.calc.display_value, "123")

    def test_input_digit_after_reset(self):
        """Ввод цифры после сброса дисплея"""
        self.calc._reset_display = True
        self.calc.input_digit("7")
        self.assertEqual(self.calc.display_value, "7")
        self.assertFalse(self.calc._reset_display)

    def test_input_digit_after_error(self):
        """Ввод цифры после ошибки"""
        self.calc._error = True
        self.calc.input_digit("9")
        self.assertEqual(self.calc.display_value, "9")
        self.assertFalse(self.calc._error)

    # Тесты ввода точки
    def test_input_dot_first_time(self):
        """Первое нажатие точки"""
        self.calc.input_dot()
        self.assertEqual(self.calc.display_value, "0.")

    def test_input_dot_append(self):
        """Добавление точки к существующему числу"""
        self.calc.display_value = "123"
        self.calc.input_dot()
        self.assertEqual(self.calc.display_value, "123.")

    def test_input_dot_already_has_dot(self):
        """Попытка добавить точку, когда она уже есть"""
        self.calc.display_value = "12.3"
        self.calc.input_dot()
        self.assertEqual(self.calc.display_value, "12.3")

    def test_input_dot_after_reset(self):
        """Ввод точки после сброса дисплея"""
        self.calc._reset_display = True
        self.calc.input_dot()
        self.assertEqual(self.calc.display_value, "0.")
        self.assertFalse(self.calc._reset_display)

    # Тесты изменения знака
    def test_toggle_sign_positive_to_negative(self):
        """Изменение положительного числа на отрицательное"""
        self.calc.display_value = "123"
        self.calc.toggle_sign()
        self.assertEqual(self.calc.display_value, "-123")

    def test_toggle_sign_negative_to_positive(self):
        """Изменение отрицательного числа на положительное"""
        self.calc.display_value = "-456"
        self.calc.toggle_sign()
        self.assertEqual(self.calc.display_value, "456")

    def test_toggle_sign_zero(self):
        """Изменение знака нуля (должен остаться нулем)"""
        self.calc.display_value = "0"
        self.calc.toggle_sign()
        self.assertEqual(self.calc.display_value, "0")

    def test_toggle_sign_after_error(self):
        """Изменение знака при ошибке (не должно работать)"""
        self.calc._error = True
        self.calc.display_value = "123"
        self.calc.toggle_sign()
        self.assertEqual(self.calc.display_value, "123")  # Не изменилось

    # Тесты backspace
    def test_backspace_normal(self):
        """Обычное удаление символа"""
        self.calc.display_value = "123"
        self.calc.backspace()
        self.assertEqual(self.calc.display_value, "12")

    def test_backspace_single_digit(self):
        """Удаление единственной цифры"""
        self.calc.display_value = "5"
        self.calc.backspace()
        self.assertEqual(self.calc.display_value, "0")

    def test_backspace_after_reset(self):
        """Backspace после сброса дисплея"""
        self.calc._reset_display = True
        self.calc.backspace()
        self.assertEqual(self.calc.display_value, "0")
        self.assertFalse(self.calc._reset_display)

    def test_backspace_after_error(self):
        """Backspace после ошибки"""
        self.calc._error = True
        self.calc.backspace()
        self.assertEqual(self.calc.display_value, "0")
        self.assertFalse(self.calc._error)

    # Тесты бинарных операций
    def test_binary_addition(self):
        """Тест сложения"""
        self.calc.display_value = "10"
        self.calc.set_operator("+")
        self.calc.display_value = "5"
        self.calc.equals()
        self.assertEqual(self.calc.display_value, "15")

    def test_binary_subtraction(self):
        """Тест вычитания"""
        self.calc.display_value = "20"
        self.calc.set_operator("-")
        self.calc.display_value = "8"
        self.calc.equals()
        self.assertEqual(self.calc.display_value, "12")

    def test_binary_multiplication(self):
        """Тест умножения"""
        self.calc.display_value = "6"
        self.calc.set_operator("*")
        self.calc.display_value = "7"
        self.calc.equals()
        self.assertEqual(self.calc.display_value, "42")

    def test_binary_division(self):
        """Тест деления"""
        self.calc.display_value = "15"
        self.calc.set_operator("/")
        self.calc.display_value = "3"
        self.calc.equals()
        self.assertEqual(self.calc.display_value, "5")

if __name__ == '__main__':
    unittest.main()