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
        self.calc.input_digit("1")
        self.calc.input_digit("2")
        self.calc.input_digit("3")
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
        self.calc.input_digit("1")
        self.calc.input_digit("2")
        self.calc.input_digit("3")
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
        self.calc.input_digit("1")
        self.calc.input_digit("2")
        self.calc.input_digit("3")
        self.calc.input_dot()
        self.assertEqual(self.calc.display_value, "123.")

    def test_input_dot_already_has_dot(self):
        """Попытка добавить точку, когда она уже есть"""
        self.calc.input_digit("1")
        self.calc.input_digit("2")
        self.calc.input_dot()
        self.calc.input_digit("3")
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
        self.calc.input_digit("1")
        self.calc.input_digit("2")
        self.calc.input_digit("3")
        self.calc.toggle_sign()
        self.assertEqual(self.calc.display_value, "-123")

    def test_toggle_sign_negative_to_positive(self):
        """Изменение отрицательного числа на положительное"""
        self.calc.display_value = "-456"
        self.calc.toggle_sign()
        self.assertEqual(self.calc.display_value, "456")

    def test_toggle_sign_zero(self):
        """Изменение знака нуля (должен остаться нулем)"""
        self.calc.input_digit("0")
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
        self.calc.input_digit("1")
        self.calc.input_digit("2")
        self.calc.input_digit("3")
        self.calc.backspace()
        self.assertEqual(self.calc.display_value, "12")

    def test_backspace_single_digit(self):
        """Удаление единственной цифры"""
        self.calc.input_digit("5")
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
        self.calc.input_digit("1")
        self.calc.input_digit("0")
        self.calc.set_operator("+")
        self.calc.input_digit("5")
        self.calc.equals()
        self.assertEqual(self.calc.display_value, "15")

    def test_binary_subtraction(self):
        """Тест вычитания"""
        self.calc.input_digit("2")
        self.calc.input_digit("0")
        self.calc.set_operator("-")
        self.calc.input_digit("8")
        self.calc.equals()
        self.assertEqual(self.calc.display_value, "12")

    def test_binary_multiplication(self):
        """Тест умножения"""
        self.calc.input_digit("6")
        self.calc.set_operator("*")
        self.calc.input_digit("7")
        self.calc.equals()
        self.assertEqual(self.calc.display_value, "42")

    def test_binary_division(self):
        """Тест деления"""
        self.calc.input_digit("1")
        self.calc.input_digit("5")
        self.calc.set_operator("/")
        self.calc.input_digit("3")
        self.calc.equals()
        self.assertEqual(self.calc.display_value, "5")

    def test_division_by_zero(self):
        """Тест деления на ноль"""
        self.calc.input_digit("1")
        self.calc.input_digit("0")
        self.calc.set_operator("/")
        self.calc.input_digit("0")
        self.calc.equals()
        self.assertEqual(self.calc.display_value, "Error")
        self.assertTrue(self.calc._error)

    def test_modulo_operation(self):
        """Тест операции взятия остатка"""
        self.calc.input_digit("1")
        self.calc.input_digit("0")
        self.calc.set_operator("%")
        self.calc.input_digit("3")
        self.calc.equals()
        self.assertEqual(self.calc.display_value, "1")

    def test_modulo_by_zero(self):
        """Тест взятия остатка от деления на ноль"""
        self.calc.input_digit("1")
        self.calc.input_digit("0")
        self.calc.set_operator("%")
        self.calc.input_digit("0")
        self.calc.equals()
        self.assertEqual(self.calc.display_value, "Error")
        self.assertTrue(self.calc._error)

    def test_power_operation(self):
        """Тест возведения в степень"""
        self.calc.input_digit("2")
        self.calc.set_operator("^")
        self.calc.input_digit("3")
        self.calc.equals()
        self.assertEqual(self.calc.display_value, "8")

    def test_chained_operations(self):
        """Тест цепочки операций"""
        # 10 + 20 - 5
        self.calc.input_digit("1")
        self.calc.input_digit("0")
        self.calc.set_operator("+")
        self.calc.input_digit("2")
        self.calc.input_digit("0")
        self.calc.set_operator("-")  # Должно вычислить 10+20=30
        self.calc.input_digit("5")
        self.calc.equals()
        self.assertEqual(self.calc.display_value, "25")

    # Тесты унарных операций
    def test_sin_operation(self):
        """Тест синуса (в градусах)"""
        self.calc.input_digit("30")
        self.calc.apply_unary("sin")
        expected = math.sin(math.radians(30))
        self.assertAlmostEqual(float(self.calc.display_value), expected, places=10)

    def test_cos_operation(self):
        """Тест косинуса (в градусах)"""
        self.calc.input_digit("60")
        self.calc.apply_unary("cos")
        expected = math.cos(math.radians(60))
        self.assertAlmostEqual(float(self.calc.display_value), expected, places=10)

    def test_sqrt_operation(self):
        """Тест квадратного корня"""
        self.calc.input_digit("16")
        self.calc.apply_unary("sqrt")
        self.assertEqual(self.calc.display_value, "4")

    def test_sqrt_negative(self):
        """Тест квадратного корня из отрицательного числа"""
        self.calc.input_digit("4")
        self.calc.toggle_sign()
        self.calc.apply_unary("sqrt")
        self.assertEqual(self.calc.display_value, "Error")
        self.assertTrue(self.calc._error)

    def test_floor_operation(self):
        """Тест округления вниз"""
        self.calc.input_digit("3")
        self.calc.input_dot()
        self.calc.input_digit("7")
        self.calc.apply_unary("floor")
        self.assertEqual(self.calc.display_value, "3")

    def test_ceil_operation(self):
        """Тест округления вверх"""
        self.calc.input_digit("3")
        self.calc.input_dot()
        self.calc.input_digit("2")
        self.calc.apply_unary("ceil")
        self.assertEqual(self.calc.display_value, "4")

    # Тесты операций с памятью
    def test_memory_clear(self):
        """Тест очистки памяти"""
        self.calc._memory = 100.0
        self.calc.memory_clear()
        self.assertEqual(self.calc._memory, 0.0)

    def test_memory_recall(self):
        """Тест извлечения из памяти"""
        self.calc._memory = 42.0
        self.calc.memory_recall()
        self.assertEqual(self.calc.display_value, "42")
        self.assertTrue(self.calc._reset_display)

    def test_memory_add(self):
        """Тест добавления к памяти"""
        self.calc._memory = 10.0
        self.calc.input_digit("5")
        self.calc.memory_add()
        self.assertEqual(self.calc._memory, 15.0)

    def test_memory_add_with_error(self):
        """Тест добавления к памяти при ошибке на дисплее"""
        self.calc._memory = 10.0
        self.calc.display_value = "Error"
        self.calc._error = True
        self.calc.memory_add()
        self.assertEqual(self.calc._memory, 10.0)  # Не изменилось

    def test_memory_subtract(self):
        """Тест вычитания из памяти"""
        self.calc._memory = 20.0
        self.calc.input_digit("7")
        self.calc.memory_subtract()
        self.assertEqual(self.calc._memory, 13.0)

    # Тесты обработки ошибок
    def test_error_state_prevents_operations(self):
        """Тест, что в состоянии ошибки многие операции не выполняются"""
        self.calc._error = True
        self.calc.display_value = "999"
        
        # Эти операции не должны выполняться при ошибке
        self.calc.toggle_sign()
        self.calc.set_operator("+")
        self.calc.apply_unary("sqrt")
        
        # Дисплей не должен измениться
        self.assertEqual(self.calc.display_value, "999")

    def test_invalid_input_handling(self):
        """Тест обработки невалидного ввода (должно вызывать ошибку)"""
        self.calc._pending_operator = "invalid_op"
        self.calc._stored_operand = 10.0
        self.calc.display_value = "5"
        
        self.calc.equals()
        self.assertEqual(self.calc.display_value, "Error")
        self.assertTrue(self.calc._error)

    # Тесты форматирования
    def test_formatting_large_number(self):
        """Тест форматирования большого числа"""
        result = self.calc._fmt(123456789.123456789)
        self.assertIn("123456789", result)
        self.assertNotIn("123456789.123456789", result)  # Должно быть сокращено

    def test_formatting_small_number(self):
        """Тест форматирования малого числа"""
        result = self.calc._fmt(0.000000123456)
        self.assertNotEqual(result, "0.000000123456")  # Должно быть сокращено

    def test_formatting_infinity(self):
        """Тест форматирования бесконечности"""
        result = self.calc._fmt(float('inf'))
        self.assertEqual(result, "Error")

    def test_formatting_nan(self):
        """Тест форматирования NaN"""
        result = self.calc._fmt(float('nan'))
        self.assertEqual(result, "Error")

    # Интеграционные тесты - сложные сценарии
    def test_complex_calculation_flow(self):
        """Тест сложного потока вычислений"""
        # ((5 + 3) * 2) / 4
        self.calc.input_digit("5")
        self.calc.set_operator("+")
        self.calc.input_digit("3")
        self.calc.set_operator("*")
        self.calc.input_digit("2")
        self.calc.set_operator("/")
        self.calc.input_digit("4")
        self.calc.equals()
        self.assertEqual(self.calc.display_value, "4")  # (5+3)*2/4 = 4

    def test_memory_integration(self):
        """Интеграционный тест с памятью"""
        # 10 + 5 = 15, сохраняем в память, затем используем
        self.calc.input_digit("1")
        self.calc.input_digit("0")
        self.calc.set_operator("+")
        self.calc.input_digit("5")
        self.calc.equals()
        
        self.calc.memory_add()  # M = 15
        self.calc.memory_recall()
        self.calc.set_operator("*")
        self.calc.input_digit("2")
        self.calc.equals()
        self.assertEqual(self.calc.display_value, "30")  # 15 * 2 = 30

if __name__ == '__main__':
    unittest.main()