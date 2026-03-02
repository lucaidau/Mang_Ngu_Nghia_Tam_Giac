from .quanLiDoThi import QuanLiDoThi


class Rules:
    def __init__(self, qldt: QuanLiDoThi):
        self.quan_li_do_thi = qldt

    """Các luật và  công thức"""

    def pytago(self):
        print("Đã áp dụng định lý Pytago")
