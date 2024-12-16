import re
from decimal import *

class Double:
    def __init__(self, value):
        if not isinstance(value, str):
            value = str(value)
            # Замена запятой на точку и удаление пробелов для дальнейшей обработки
        value = value.replace(',', '.')
            
            # Проверка корректности ввода с использованием пробелов для разделения тысячных разрядов
            # Формат: допускаются группы по 3 цифры, разделенные одним пробелом
        if not re.match(r'^[+-]?(\d{1,3}( \d{3})*|\d+)(\.\d*)?$', value):
            raise ValueError("Invalid format for Double initialization")
            
        self.value = Decimal(value.replace(' ', ''))

    @staticmethod
    def format_number(value):
        """
        Форматирует Decimal или число с разделением разрядов пробелами.
        """
        int_part, _, frac_part = str(value.normalize()).partition(".")
        int_part = f"{int(int_part):,}".replace(",", " ")  # Разделение разрядов
        if frac_part:
            return f"{int_part}.{frac_part}"
        return int_part
    
    
    def __str__(self):
        """
        Возвращает строковое представление числа с разделением разрядов пробелами 
        и ограничением до 6 знаков после запятой, без лишних нулей.
        """
        # Сохраняем знак числа
        sign = "-" if self.value < 0 else ""
        abs_value = abs(self.value)

        # Ограничение до 6 знаков после запятой
        abs_value = abs_value.quantize(Decimal("1.000000"), rounding=ROUND_HALF_UP).normalize()

        # Разделяем на целую и дробную части
        int_part, _, frac_part = str(abs_value).partition(".")
        int_part = f"{int(int_part):,}".replace(",", " ")  # Разделение разрядов целой части пробелами

        if frac_part:  # Если есть дробная часть
            return f"{sign}{int_part}.{frac_part}"
        return f"{sign}{int_part}"

    def __add__(self, other):
        """
        Сложение двух объектов Double.
        """
        if not isinstance(other, Double):
            raise TypeError("Addition only supports Double")
        return Double(self.value + other.value)

    def __sub__(self, other):
        """
        Вычитание двух объектов Double.
        """
        if not isinstance(other, Double):
            raise TypeError("Subtraction only supports Double")
        return Double(self.value - other.value)

    def __mul__(self, other):
        """
        Умножение двух объектов Double.
        """
        if not isinstance(other, Double):
            raise TypeError("Multiplication only supports Double")
        return Double(self.value * other.value)

    def __truediv__(self, other):
        """
        Деление двух объектов Double.
        """
        if not isinstance(other, Double):
            raise TypeError("Division only supports Double")
        if other.value == 0:
            raise ZeroDivisionError("Division by zero")
        return Double(self.value / other.value)
    
    def round_to_integer(self, method="математическое"):
        """
        Округляет число до целого по выбранному методу:
        - "математическое": стандартное округление (по правилам).
        - "бухгалтерское": округление к ближайшему чётному.
        - "усечение": округление вниз.
        """
        if method == "математическое":
            # Математическое округление
            return int(self.value.to_integral_value(rounding=ROUND_HALF_UP))
        elif method == "бухгалтерское":
            # Бухгалтерское округление (к ближайшему чётному)
            return int(self.value.to_integral_value(rounding=ROUND_HALF_EVEN))
        elif method == "усечение":
            # Усечение (округление вниз)
            return int(self.value.to_integral_value(rounding=ROUND_DOWN))
        else:
            raise ValueError(f"Unsupported rounding method: {method}")

