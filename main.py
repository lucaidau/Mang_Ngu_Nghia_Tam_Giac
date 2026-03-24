import tkinter as tk
from app.models.quanLiDoThi import QuanLiDoThi
from app.views.giaoDienChinh import GiaoDienChinh
from app.controllers.controller import Controller


def main():
    root = tk.Tk()
    app_model = QuanLiDoThi()
    app_view = GiaoDienChinh(root)
    app_controller = Controller(model=app_model, view=app_view)

    root.mainloop()

if __name__ == "__main__":
    main()
