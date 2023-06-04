import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
import sqlite3
import tkinter.ttk as ttk


class Product:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity


class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, name, quantity, person):
        product = Product(name, quantity)
        self.products.append(product)
        self.save_product(name, quantity, person, 'Добавление')

    def remove_product(self, name, quantity, person):
        for product in self.products:
            if product.name == name:
                if product.quantity >= quantity:
                    product.quantity -= quantity
                    self.save_product(name, quantity, person, 'Изъятие')
                else:
                    messagebox.showerror("Ошибка", f"Недостаточное количество товара '{name}' на складе.")
                return
        messagebox.showerror("Ошибка", f"Продукт '{name}' не найден на складе.")

    def save_product(self, name, quantity, person, action):
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        date = datetime.date.today()
        c.execute("INSERT INTO products (name, quantity, person, action, date) VALUES (?, ?, ?, ?, ?)",
                  (name, quantity, person, action, date))
        conn.commit()
        conn.close()

    def get_inventory_summary(self):
        summary = {}
        for product in self.products:
            if product.name in summary:
                summary[product.name] += product.quantity
            else:
                summary[product.name] = product.quantity
        return summary


class InventoryApp:
    def __init__(self):
        self.inventory = Inventory()
        self.window = tk.Tk()
        self.window.title("Inventory App")
        self.window.configure(bg="white")
        self.window.geometry("1920x1080")
        self.load_styles()
        self.create_widgets()
        self.window.bind('<Configure>', self.update_button_styles)

    def load_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("App.TButton", filename="styles.css")
        style.configure("App.TLabel", filename="styles.css")

    def create_widgets(self):
        self.add_product_button = ttk.Button(self.window, text="Добавить товар", command=self.show_add_product_dialog,
                                             style="App.TButton")
        self.add_product_button.pack(pady=10, padx=20)
        self.add_product_button.bind('<Enter>', self.highlight_button)
        self.add_product_button.bind('<Leave>', self.restore_button)

        self.remove_product_button = ttk.Button(self.window, text="Изъять товар", command=self.show_remove_product_dialog,
                                                style="App.TButton")
        self.remove_product_button.pack(pady=10, padx=20)
        self.remove_product_button.bind('<Enter>', self.highlight_button)
        self.remove_product_button.bind('<Leave>', self.restore_button)

        self.inventory_summary_button = ttk.Button(self.window, text="Остаток", command=self.show_inventory_summary,
                                                   style="App.TButton")
        self.inventory_summary_button.pack(pady=10, padx=20)
        self.inventory_summary_button.bind('<Enter>', self.highlight_button)
        self.inventory_summary_button.bind('<Leave>', self.restore_button)

        self.statistics_button = ttk.Button(self.window, text="Статистика", command=self.show_statistics_dialog,
                                            style="App.TButton")
        self.statistics_button.pack(pady=10, padx=20)
        self.statistics_button.bind('<Enter>', self.highlight_button)
        self.statistics_button.bind('<Leave>', self.restore_button)

    def show_add_product_dialog(self):
        dialog = AddProductDialog(self.window, self.inventory)
        self.window.wait_window(dialog.top)

    def show_remove_product_dialog(self):
        dialog = RemoveProductDialog(self.window, self.inventory)
        self.window.wait_window(dialog.top)

    def show_inventory_summary(self):
        summary = self.inventory.get_inventory_summary()
        table = ttk.Treeview(self.window)
        table["columns"] = ("name", "quantity")
        table.heading("name", text="Наименование")
        table.heading("quantity", text="Количество")
        for product, quantity in summary.items():
            table.insert("", tk.END, values=(product, quantity))
        table.pack()

    def show_statistics_dialog(self):
        dialog = StatisticsDialog(self.window)
        self.window.wait_window(dialog.top)

    def highlight_button(self, event):
        event.widget['style'] = 'Highlighted.TButton'

    def restore_button(self, event):
        event.widget['style'] = 'App.TButton'

    def update_button_styles(self, event):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        if width <= 500:
            self.add_product_button.configure(width=80)
            self.remove_product_button.configure(width=80)
            self.inventory_summary_button.configure(width=80)
            self.statistics_button.configure(width=80)
        else:
            self.add_product_button.configure(width=100)
            self.remove_product_button.configure(width=100)
            self.inventory_summary_button.configure(width=100)
            self.statistics_button.configure(width=100)


class AddProductDialog:
    def __init__(self, parent, inventory):
        self.inventory = inventory
        self.top = tk.Toplevel(parent)
        self.top.title("Добавление товара")
        self.name_label = ttk.Label(self.top, text="Название товара:")
        self.name_label.pack(pady=5)
        self.name_entry = ttk.Entry(self.top)
        self.name_entry.pack(pady=5)
        self.quantity_label = ttk.Label(self.top, text="Количество:")
        self.quantity_label.pack(pady=5)
        self.quantity_entry = ttk.Entry(self.top)
        self.quantity_entry.pack(pady=5)
        self.person_label = ttk.Label(self.top, text="Ответственное лицо:")
        self.person_label.pack(pady=5)
        self.person_entry = ttk.Entry(self.top)
        self.person_entry.pack(pady=5)
        self.add_button = ttk.Button(self.top, text="Добавить", command=self.add_product)
        self.add_button.pack(pady=10)

    def add_product(self):
        name = self.name_entry.get()
        quantity = int(self.quantity_entry.get())
        person = self.person_entry.get()
        if name and quantity and person:
            self.inventory.add_product(name, quantity, person)
            messagebox.showinfo("Успех", f"Товар '{name}' успешно добавлен на склад.")
            self.top.destroy()
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")


class RemoveProductDialog:
    def __init__(self, parent, inventory):
        self.inventory = inventory
        self.top = tk.Toplevel(parent)
        self.top.title("Изъятие товара")
        self.name_label = ttk.Label(self.top, text="Название товара:")
        self.name_label.pack(pady=5)
        self.name_combobox = Combobox(self.top, values=self.get_product_names())
        self.name_combobox.pack(pady=5)
        self.quantity_label = ttk.Label(self.top, text="Количество:")
        self.quantity_label.pack(pady=5)
        self.quantity_entry = ttk.Entry(self.top)
        self.quantity_entry.pack(pady=5)
        self.person_label = ttk.Label(self.top, text="Ответственное лицо:")
        self.person_label.pack(pady=5)
        self.person_entry = ttk.Entry(self.top)
        self.person_entry.pack(pady=5)
        self.remove_button = ttk.Button(self.top, text="Изъять", command=self.remove_product)
        self.remove_button.pack(pady=10)

    def get_product_names(self):
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT DISTINCT name FROM products")
        product_names = [row[0] for row in c.fetchall()]
        conn.close()
        return product_names

    def remove_product(self):
        name = self.name_combobox.get()
        quantity = int(self.quantity_entry.get())
        person = self.person_entry.get()
        if name and quantity and person:
            self.inventory.remove_product(name, quantity, person)
            messagebox.showinfo("Успех", f"Товар '{name}' успешно изъят со склада.")
            self.top.destroy()
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")


class StatisticsDialog:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Статистика")
        self.load_statistics()

    def load_statistics(self):
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        data = c.fetchall()
        table = ttk.Treeview(self.top)
        table["columns"] = ("name", "quantity", "person", "action", "date")
        table.heading("name", text="Наименование")
        table.heading("quantity", text="Количество")
        table.heading("person", text="Ответственное лицо")
        table.heading("action", text="Действие")
        table.heading("date", text="Дата")
        for row in data:
            table.insert("", tk.END, values=row)
        table.pack()
        conn.close()


if __name__ == "__main__":
    app = InventoryApp()
    app.window.state('zoomed')
    app.window.mainloop()
