import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Double import Double

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор с четырьмя операндами")

        # Инициализация переменных
        self.operand1 = tk.StringVar(value="0")
        self.operand2 = tk.StringVar(value="0")
        self.operand3 = tk.StringVar(value="0")
        self.operand4 = tk.StringVar(value="0")
        self.operation1 = tk.StringVar(value="+")
        self.operation2 = tk.StringVar(value="+")
        self.operation3 = tk.StringVar(value="+")
        self.result = tk.StringVar(value="Результат")

        self.rounding_method = tk.StringVar(value="математическое")
        self.rounded_result = tk.StringVar(value="Округленный до целых результат")

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(column=0, row=0, sticky="NSEW")

        # Поля ввода
        ttk.Label(frame, text="Число 1").grid(column=0, row=0, sticky="W")
        ttk.Entry(frame, textvariable=self.operand1).grid(column=1, row=0)

        ttk.Combobox(frame, textvariable=self.operation1, values=["+", "-", "*", "/"]).grid(column=2, row=0)

        ttk.Label(frame, text="(").grid(column=3, row=0)

        ttk.Entry(frame, textvariable=self.operand2).grid(column=4, row=0)
        ttk.Combobox(frame, textvariable=self.operation2, values=["+", "-", "*", "/"]).grid(column=5, row=0)
        ttk.Entry(frame, textvariable=self.operand3).grid(column=6, row=0)

        ttk.Label(frame, text=")").grid(column=7, row=0)

        ttk.Combobox(frame, textvariable=self.operation3, values=["+", "-", "*", "/"]).grid(column=8, row=0)
        ttk.Entry(frame, textvariable=self.operand4).grid(column=9, row=0)

        # Кнопка для вычисления
        ttk.Button(frame, text="=", command=self.calculate).grid(column=10, row=0)

        # Отображение результата
        ttk.Label(frame, textvariable=self.result, font=("Arial", 14)).grid(column=0, row=1, columnspan=11, sticky="W")

        # Выбор вида округления
        ttk.Label(frame, text="Выбор вида округления:").grid(column=0, row=2, columnspan=4, sticky="W")
        ttk.Radiobutton(frame, text="Математическое", variable=self.rounding_method, value="математическое").grid(column=0, row=3, columnspan=4, sticky="W")
        ttk.Radiobutton(frame, text="Бухгалтерское", variable=self.rounding_method, value="бухгалтерское").grid(column=0, row=4, columnspan=4, sticky="W")
        ttk.Radiobutton(frame, text="Усечение", variable=self.rounding_method, value="усечение").grid(column=0, row=5, columnspan=4, sticky="W")

        # Отображение округленного результата
        ttk.Label(frame, textvariable=self.rounded_result, font=("Arial", 14)).grid(column=0, row=6, columnspan=11, sticky="W")
        ttk.Label(frame, text="Юревич А.Н., 3 курс, 11 группа, 2024").grid(column=0, row=7, sticky="W")

    def calculate(self):
        try:
            # Считываем операнды
            op1 = Double(self.operand1.get())
            op2 = Double(self.operand2.get())
            op3 = Double(self.operand3.get())
            op4 = Double(self.operand4.get())

            # Выполняем приоритетную операцию
            intermediate_result = self.perform_operation(op2, op3, self.operation2.get())

            # Выполняем остальные операции
            result = self.perform_operation(op1, intermediate_result, self.operation1.get())
            result = self.perform_operation(result, op4, self.operation3.get())

            # Округляем результат
            self.result.set(f"Результат вычисления: {result}")
            rounded = result.round_to_integer(self.rounding_method.get())
            self.rounded_result.set(f"Округленный до целых: {rounded}")

        except Exception as e:
            self.result.set(f"Ошибка: {e}")

    def perform_operation(self, operand1, operand2, operation):
        if operation == "+":
            return operand1 + operand2
        elif operation == "-":
            return operand1 - operand2
        elif operation == "*":
            return operand1 * operand2
        elif operation == "/":
            return operand1 / operand2
        else:
            raise ValueError(f"Неверная операция: {operation}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()