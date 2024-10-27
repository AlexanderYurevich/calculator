import re

class Double:
    def __init__(self, value):
        if isinstance(value, str):
            # Заменяем запятую на точку для унификации
            value = value.replace(',', '.')
            
            # Проверка, что строка содержит число с десятичной точкой
            if re.match(r'^[+-]?\d+(\.\d*)?$', value):
                # Находим позицию точки, если есть
                point_index = value.find('.')
                
                # Определяем масштаб (количество знаков после точки)
                self.scale = len(value) - point_index - 1 if point_index != -1 else 0
                
                # Убираем точку, если она есть, и сохраняем значение как целое число
                self.value = int(value.replace('.', ''))
            else:
                raise ValueError("Invalid value for Double initialization")
        else:
            raise ValueError("Unsupported type for Double initialization")

    def __str__(self):
        # Преобразуем значение обратно в строку с учетом масштаба
        value_str = str(abs(self.value))  # Абсолютное значение для обработки строки
        sign = '-' if self.value < 0 else ''  # Сохраняем знак числа
        
        # Если масштаб равен нулю, возвращаем целое число
        if self.scale == 0:
            return sign + value_str
        
        # Вставляем точку перед нужной позицией, добавляем нули, если нужно
        if len(value_str) <= self.scale:
            value_str = '0' * (self.scale + 1 - len(value_str)) + value_str
        
        # Формируем строку с десятичной точкой
        formatted_value = value_str[:-self.scale] + '.' + value_str[-self.scale:]
        
        # Убираем незначащие нули справа и возвращаем результат с учетом знака
        return sign + formatted_value.rstrip('0').rstrip('.') if '.' in formatted_value else sign + formatted_value

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

    def __truediv__(self, other):
        if isinstance(other, Double):
            if other.value == 0:
                raise ZeroDivisionError("Division by zero")
            
            # Для деления увеличиваем масштаб результата для лучшей точности
            extended_scale = self.scale + other.scale + 10
            dividend = self.value * (10 ** extended_scale)
            result_value = dividend // other.value
            return Double.from_int(result_value, extended_scale - other.scale)
        raise ValueError("Division is only supported between Double instances")

    @classmethod
    def from_int(cls, value, scale):
        """Метод для создания объекта Double из целого числа и масштаба."""
        obj = cls.__new__(cls)
        obj.value = value
        obj.scale = scale
        return obj
