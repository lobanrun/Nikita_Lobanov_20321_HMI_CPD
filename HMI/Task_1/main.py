import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from datetime import datetime


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Учет расходов")
        self.root.geometry("1200x1200")

        self.expenses = []
        self.sort_ascending_date = True  # Флаг для отслеживания порядка сортировки по дате
        self.sort_ascending_category = True  # Флаг для отслеживания порядка сортировки по категории
        self.sort_ascending_amount = True  # Флаг для отслеживания порядка сортировки по сумме

        # Поля для ввода данных
        self.date_label = tk.Label(root, text="Дата:")
        self.date_label.grid(row=0, column=0, padx=10, pady=10)
        self.date_entry = DateEntry(root, date_pattern="dd.mm.yyyy")
        self.date_entry.grid(row=0, column=1, padx=10, pady=10)

        self.category_label = tk.Label(root, text="Категория:")
        self.category_label.grid(row=1, column=0, padx=10, pady=10)
        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=1, column=1, padx=10, pady=10)

        self.amount_label = tk.Label(root, text="Сумма:")
        self.amount_label.grid(row=2, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=10)

        # Кнопка для добавления записи
        self.add_button = tk.Button(root, text="Добавить запись", command=self.add_expense)
        self.add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Таблица для отображения расходов с возможностью сортировки по всем столбцам
        self.tree = ttk.Treeview(root, columns=("Дата", "Категория", "Сумма"), show="headings")
        self.tree.heading("Дата", text="Дата", command=self.sort_by_date)
        self.tree.heading("Категория", text="Категория", command=self.sort_by_category)
        self.tree.heading("Сумма", text="Сумма", command=self.sort_by_amount)
        self.tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Кнопка для удаления записи
        self.delete_button = tk.Button(root, text="Удалить запись", command=self.delete_expense)
        self.delete_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # График расходов
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Загрузка данных из файла
        self.load_expenses()

    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму")
            return

        self.expenses.append((date, category, amount))
        self.tree.insert("", "end", values=(date, category, amount))
        self.save_expenses()
        self.update_chart()

    def delete_expense(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            values = item["values"]
            self.expenses.remove((values[0], values[1], float(values[2])))
            self.tree.delete(selected_item)
            self.save_expenses()
            self.update_chart()
        else:
            messagebox.showerror("Ошибка", "Выберите запись для удаления")

    def update_chart(self):
        categories = {}
        for _, category, amount in self.expenses:
            categories[category] = categories.get(category, 0) + amount

        self.ax.clear()
        self.ax.bar(categories.keys(), categories.values())
        self.ax.set_title("Расходы по категориям")
        self.ax.set_xlabel("Категория")
        self.ax.set_ylabel("Сумма")
        self.canvas.draw()

    def save_expenses(self):
        with open("expenses.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.expenses)

    def load_expenses(self):
        try:
            with open("expenses.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    date, category, amount = row
                    self.expenses.append((date, category, float(amount)))
                    self.tree.insert("", "end", values=(date, category, amount))
            self.update_chart()
        except FileNotFoundError:
            pass

    def sort_by_date(self):
        # Сортировка списка расходов по дате
        self.expenses.sort(key=lambda x: datetime.strptime(x[0], "%d.%m.%Y"), reverse=not self.sort_ascending_date)
        self.sort_ascending_date = not self.sort_ascending_date  # Переключение флага сортировки

        # Обновление таблицы с отсортированными данными
        self.update_tree()

    def sort_by_category(self):
        # Сортировка списка расходов по категории
        self.expenses.sort(key=lambda x: x[1], reverse=not self.sort_ascending_category)
        self.sort_ascending_category = not self.sort_ascending_category  # Переключение флага сортировки

        # Обновление таблицы с отсортированными данными
        self.update_tree()

    def sort_by_amount(self):
        # Сортировка списка расходов по сумме
        self.expenses.sort(key=lambda x: x[2], reverse=not self.sort_ascending_amount)
        self.sort_ascending_amount = not self.sort_ascending_amount  # Переключение флага сортировки

        # Обновление таблицы с отсортированными данными
        self.update_tree()

    def update_tree(self):
        # Очистка таблицы и вставка отсортированных данных
        for row in self.tree.get_children():
            self.tree.delete(row)
        for expense in self.expenses:
            self.tree.insert("", "end", values=expense)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()

