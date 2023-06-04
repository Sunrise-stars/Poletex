import tkinter as tk
from tkinter import messagebox

class AuthorizationDialog:
    def __init__(self, parent, on_success):
        self.parent = parent
        self.on_success = on_success
        self.top = tk.Toplevel(parent)
        self.top.title("Авторизация")
        self.top.geometry("1980x1080")
        self.username_label = tk.Label(self.top, text="Имя пользователя:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.top)
        self.username_entry.pack(pady=5)
        self.password_label = tk.Label(self.top, text="Пароль:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.top, show="*")
        self.password_entry.pack(pady=5)
        self.login_button = tk.Button(self.top, text="Войти", command=self.login)
        self.login_button.pack(pady=10)
        self.register_button = tk.Button(self.top, text="Зарегистрироваться", command=self.register)
        self.register_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            # Здесь можно добавить логику проверки авторизации
            self.on_success()
            self.top.destroy()
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            # Здесь можно добавить логику регистрации
            self.on_success(username, password)
            self.top.destroy()
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")

def authorize(on_authorization_success, on_registration_success):
    root = tk.Tk()
    root.withdraw()
    dialog = AuthorizationDialog(root, on_authorization_success)
    root.mainloop()
