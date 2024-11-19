import tkinter as tk
from tkinter import messagebox
from Double import Double

class CalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Калькулятор")

        # Устанавливаем конфигурацию для адаптации
        master.grid_rowconfigure(0, weight=1)
        for i in range(9):
            master.grid_rowconfigure(i, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # Ввод первого числа
        self.label1 = tk.Label(master, text="Введите первое число:")
        self.label1.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
        
        self.entry1 = tk.Entry(master)
        self.entry1.grid(row=1, column=0, sticky='ew', padx=10, pady=5)
        self.create_context_menu(self.entry1)  # Контекстное меню для первого поля ввода

        # Ввод второго числа
        self.label2 = tk.Label(master, text="Введите второе число:")
        self.label2.grid(row=2, column=0, sticky='ew', padx=10, pady=5)
        
        self.entry2 = tk.Entry(master)
        self.entry2.grid(row=3, column=0, sticky='ew', padx=10, pady=5)
        self.create_context_menu(self.entry2)  # Контекстное меню для второго поля ввода

        # Радиокнопки для операций
        self.operation_var = tk.StringVar(value="add")  # Сложение по умолчанию

        self.add_radio = tk.Radiobutton(master, text="Сложение", variable=self.operation_var, value="add")
        self.add_radio.grid(row=4, column=0, sticky='ew', padx=10, pady=5)

        self.subtract_radio = tk.Radiobutton(master, text="Вычитание", variable=self.operation_var, value="subtract")
        self.subtract_radio.grid(row=5, column=0, sticky='ew', padx=10, pady=5)

        self.multiply_radio = tk.Radiobutton(master, text="Умножение", variable=self.operation_var, value="multiply")
        self.multiply_radio.grid(row=6, column=0, sticky='ew', padx=10, pady=5)

        self.divide_radio = tk.Radiobutton(master, text="Деление", variable=self.operation_var, value="divide")
        self.divide_radio.grid(row=7, column=0, sticky='ew', padx=10, pady=5)

        # Кнопка для вычисления
        self.calculate_button = tk.Button(master, text="Вычислить", command=self.calculate)
        self.calculate_button.grid(row=8, column=0, sticky='ew', padx=10, pady=5)

        # Поле для результата
        self.result_label = tk.Label(master, text="Результат:")
        self.result_label.grid(row=9, column=0, sticky='ew', padx=10, pady=5)

        self.result = tk.Label(master, text="")
        self.result.grid(row=10, column=0, sticky='ew', padx=10, pady=5)

    def create_context_menu(self, entry):
        """Создает контекстное меню для копирования, вырезания и вставки."""
        menu = tk.Menu(entry, tearoff=0)
        menu.add_command(label="Копировать", command=lambda: entry.event_generate("<<Copy>>"))
        menu.add_command(label="Вырезать", command=lambda: entry.event_generate("<<Cut>>"))
        menu.add_command(label="Вставить", command=lambda: entry.event_generate("<<Paste>>"))
        
        def show_context_menu(event):
            menu.tk_popup(event.x_root, event.y_root)

        entry.bind("<Button-3>", show_context_menu)  # ПКМ для вызова меню

    def calculate(self):
        try:
            num1 = Double(self.entry1.get())
            num2 = Double(self.entry2.get())
            operation = self.operation_var.get()
            if operation == "add":
                result = num1 + num2
            elif operation == "subtract":
                result = num1 - num2
            elif operation == "multiply":
                result = num1 * num2
            elif operation == "divide":
                result = num1 / num2

            self.result.config(text=str(result))
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Деление на ноль!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
