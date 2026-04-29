import tkinter as tk
from app.views.giaoDienChinh import GiaoDienChinh
from app.controllers.controller import Controller

def main():
    root = tk.Tk()
    root.title("Phần mềm Giải Toán Tam Giác")

    # 1. Khởi tạo View trước
    app_view = GiaoDienChinh(root, controller=None)
    
    # 2. Khởi tạo Controller (Model đã được tạo bên trong Controller rồi)
    app_controller = Controller(view=app_view)
    
    # 3. Kết nối ngược lại cho View
    app_view.controller = app_controller
    
    # 4. Chạy ứng dụng
    root.mainloop()

if __name__ == "__main__":
    main()
