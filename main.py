import authorization
from inventory_app import InventoryApp

def on_authorization_success():
    app = InventoryApp()
    app.window.mainloop()

def on_registration_success(username, password):
    # Здесь можно добавить логику сохранения нового пользователя
    messagebox.showinfo("Успех", f"Пользователь '{username}' успешно зарегистрирован.")

authorization.authorize(on_authorization_success, on_registration_success)

if __name__ == "__main__":
    app = InventoryApp()
    app.window.mainloop()
