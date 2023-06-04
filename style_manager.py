import tkinter as tk
from tkinter import ttk


class StyleManager:
    @staticmethod
    def load_styles():
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TLabel", font=("Arial", 14), foreground="#333333")
        style.configure("TButton", font=("Arial", 14), background="#4CAF50", foreground="#FFFFFF", padding=8, border=0, cursor="hand2")
        style.map("TButton", background=[("pressed", "#45a049")])
        style.configure("TEntry", font=("Arial", 14), padding=4, border=1, relief="solid")
        style.configure("TCombobox", font=("Arial", 14), padding=4, border=1, relief="solid", width=150)
