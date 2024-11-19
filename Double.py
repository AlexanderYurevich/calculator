import re

class Double:
    def __init__(self, value):
        if isinstance(value, str):
            # Замена запятой на точку и удаление пробелов для дальнейшей обработки
            value = value.replace(',', '.')
            
            # Проверка корректности ввода с использованием пробелов для разделения тысячных разрядов
            # Формат: допускаются группы по 3 цифры, разделенные одним пробелом
            if not re.match(r'^[+-]?(\d{1,3}( \d{3})*|\d+)(\.\d*)?$', value):
                raise ValueError("Invalid format for Double initialization")
            
            # Определяем позицию точки, если есть, для определения масштаба
            point_index = value.find('.')
            self.scale = len(value) - point_index - 1 if point_index != -1 else 0
            
            # Убираем точку и пробелы, сохраняем значение как целое число
            self.value = int(value.replace('.', '').replace(' ', ''))
        else:
            raise ValueError("Unsupported type for Double initialization")


    def __str__(self):
        # Абсолютное значение для форматирования строки и знак числа
        value_str = str(abs(self.value))
        sign = '-' if self.value < 0 else ''
        
        # Формирование целой и дробной части
        if self.scale == 0:
            # Форматирование целой части с пробелами
            integer_part = "{:,}".format(int(value_str)).replace(',', ' ')
            return f"{sign}{integer_part}"

        # Если длина строки меньше масштаба, добавляем нули слева
        if len(value_str) <= self.scale:
            value_str = '0' * (self.scale + 1 - len(value_str)) + value_str

        integer_part = value_str[:-self.scale] if self.scale != len(value_str) else '0'
        fractional_part = value_str[-self.scale:]

        # Форматирование целой части с пробелами и удаление незначащих нулей справа
        integer_part = "{:,}".format(int(integer_part)).replace(',', ' ')
        fractional_part = fractional_part.rstrip('0')
        
        # Формируем окончательное представление с учетом знака
        return f"{sign}{integer_part}.{fractional_part}" if fractional_part else f"{sign}{integer_part}"

    def _align_scales(self, other):
        """Вспомогательная функция для выравнивания масштаба перед арифметическими операциями."""
        if self.scale > other.scale:
            factor = 10 ** (self.scale - other.scale)
            return self.value, other.value * factor, self.scale
        elif self.scale < other.scale:
            factor = 10 ** (other.scale - self.scale)
            return self.value * factor, other.value, other.scale
        return self.value, other.value, self.scale

    def __add__(self, other):
        if isinstance(other, Double):
            aligned_self, aligned_other, result_scale = self._align_scales(other)
            result_value = aligned_self + aligned_other
            return Double.from_int(result_value, result_scale)
        raise ValueError("Addition is only supported between Double instances")

    def __sub__(self, other):
        if isinstance(other, Double):
            aligned_self, aligned_other, result_scale = self._align_scales(other)
            result_value = aligned_self - aligned_other
            return Double.from_int(result_value, result_scale)
        raise ValueError("Subtraction is only supported between Double instances")

    def __mul__(self, other):
        if isinstance(other, Double):
            result_value = self.value * other.value
            result_scale = self.scale + other.scale
            return Double.from_int(result_value, result_scale)
        raise ValueError("Multiplication is only supported between Double instances")

    def __truediv__(self, other, precision=10):
        if isinstance(other, Double):
            if other.value == 0:
                raise ZeroDivisionError("Division by zero")
            
            # Увеличиваем масштаб результата для округления до нужной точности
            extended_scale = self.scale + other.scale + precision + 1
            dividend = self.value * (10 ** extended_scale)
            result_value = dividend // other.value

            # Округление по правилам математики
            if (result_value % 10) >= 5:
                result_value += 10
            result_value //= 10
                
            return Double.from_int(result_value, extended_scale-other.scale-1+self.scale)
        raise ValueError("Division is only supported between Double instances")
    
    def round_to_integer(self, method="математическое"):
        """
        Округляет число до целых с использованием указанного метода.
        - 'математическое': стандартное математическое округление.
        - 'бухгалтерское': округление к ближайшему четному.
        - 'усечение': округление вниз (trunc).
        """
        integer_part = self.value // (10 ** self.scale)
        if integer_part < 0:
            integer_part += 1
        fractional_part = abs(self.value) % (10 ** self.scale)

        if method == "математическое":
            # Математическое округление
            if fractional_part >= 5 * (10 ** (self.scale - 1)):
                return integer_part + (1 if self.value > 0 else -1)
                
            return integer_part

       
        elif method == "бухгалтерское":
            # Бухгалтерское округление (к ближайшему чётному)
            round_up = fractional_part > 5 * (10 ** (self.scale - 1)) or (
                fractional_part == 5 * (10 ** (self.scale - 1)) and integer_part % 2 != 0
            )
            return integer_part + (1 if round_up and self.value > 0 else -1 if round_up and self.value < 0 else 0)


        elif method == "усечение":
            # Усечение (округление вниз)
            return integer_part

        else:
            raise ValueError(f"Unsupported rounding method: {method}")

    @classmethod
    def from_int(cls, value, scale):
        """Метод для создания объекта Double из целого числа и масштаба."""
        obj = cls.__new__(cls)
        obj.value = value
        obj.scale = scale
        return obj

