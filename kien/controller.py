# controller.py
from congThuc import Rules
from quanLiDoThi import QuanLiDoThi

class TriangleController:
    def __init__(self):
        pass

    def execute_logic(self, input_data):
        dt = QuanLiDoThi()
        # Đưa dữ liệu từ View vào Model
        for key, val in input_data.items():
            if val:
                dt.set(key, float(val))

        # Chạy suy luận
        rules = Rules(dt)
        rules.execute_alt()
        
        return dt # Trả về đối tượng đã tính toán xong