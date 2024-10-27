import tkinter as tk
from tkinter import messagebox
from Double import Double

class CalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Калькулятор")

        # Устанавливаем конфигурацию для адаптации
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=1)
        master.grid_rowconfigure(2, weight=1)
        master.grid_rowconfigure(3, weight=1)
        master.grid_rowconfigure(4, weight=1)
        master.grid_columnconfigure(0, weight=1)
        
        # Ввод первого числа
        self.label1 = tk.Label(master, text="Введите первое число:")
        self.label1.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
        
        self.entry1 = tk.Entry(master)
        self.entry1.grid(row=1, column=0, sticky='ew', padx=10, pady=5)

        # Ввод второго числа
        self.label2 = tk.Label(master, text="Введите второе число:")
        self.label2.grid(row=2, column=0, sticky='ew', padx=10, pady=5)
        
        self.entry2 = tk.Entry(master)
        self.entry2.grid(row=3, column=0, sticky='ew', padx=10, pady=5)

        # Радиокнопки для операций
        self.operation_var = tk.StringVar(value="add")  # Сложение по умолчанию

        self.add_radio = tk.Radiobutton(master, text="Сложение", variable=self.operation_var, value="add")
        self.add_radio.grid(row=4, column=0, sticky='ew', padx=10, pady=5)

        self.subtract_radio = tk.Radiobutton(master, text="Вычитание", variable=self.operation_var, value="subtract")
        self.subtract_radio.grid(row=5, column=0, sticky='ew', padx=10, pady=5)

        # Кнопка для вычисления
        self.calculate_button = tk.Button(master, text="Вычислить", command=self.calculate)
        self.calculate_button.grid(row=6, column=0, sticky='ew', padx=10, pady=5)

        # Поле для результата
        self.result_label = tk.Label(master, text="Результат:")
        self.result_label.grid(row=7, column=0, sticky='ew', padx=10, pady=5)

        self.result = tk.Label(master, text="")
        self.result.grid(row=8, column=0, sticky='ew', padx=10, pady=5)

    def calculate(self):
        try:
            num1 = Double(self.entry1.get())
            num2 = Double(self.entry2.get())
            if self.operation_var.get() == "add":
                result = num1 + num2
            else:
                result = num1 - num2

            self.result.config(text=str(result))
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Деление на ноль!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()