import tkinter as tk
from tkinter import ttk, messagebox
from .giaoDienDoThi import GiaoDienDoThi


class GiaoDienChinh:
    def __init__(self, root):
        self.root = root
        self.root.title("Mạng ngữ nghĩa tam giác")
        self.root.geometry("1000x600")


if __name__ == "__main__":
    root = tk.Tk()
    app = GiaoDienChinh(root)
    root.mainloop()