import tkinter as tk
from app.models.quanLiDoThi import QuanLiDoThi
from app.views.giaoDienChinh import GiaoDienChinh
from app.controllers.controller import GeometryController


def main():
    root = tk.Tk()
    app_model = QuanLiDoThi()

    app_view = GiaoDienChinh(root, controller=None)

    app_controller = GeometryController(view=app_view)
    app_view.controller = app_controller
    app_controller.qldt = app_model

    root.mainloop()


if __name__ == "__main__":
    main()
