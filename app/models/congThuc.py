import math
from .quanLiDoThi import QuanLiDoThi

class Rules:
    def __init__(self, qldt: QuanLiDoThi):
        self.quan_li_do_thi = qldt

    def execute_alt(self):
        has_changed = True

        while has_changed:
            so_not_cu = len(self.quan_li_do_thi.lay_do_thi().nodes)
            so_canh_cu = len(self.quan_li_do_thi.lay_do_thi().edges)
 
            self.tong3goc,
            self.dieu_tich_tam_giac,
            self.dinh_ly_sin,
            self.pytago,
            # Thêm các công thức khác vào đây   

            so_not_moi = len(self.quan_li_do_thi.lay_do_thi().nodes)
            so_canh_moi = len(self.quan_li_do_thi.lay_do_thi().edges)

            if so_not_cu == so_not_moi and so_canh_cu == so_canh_moi:
                has_changed = False
        
    """Các luật và  công thức"""

    def tong3goc(self):
        """ A + B + C = 180 độ"""
        v = self.quan_li_do_thi
        if v.get("A") and v.get("B") and not v.get("C"):
            v.set("C", 180 - v.get("A") - v.get("B"))
            return True
        if v.get("A") and not v.get("B") and v.get("C"):
            v.set("B", 180 - v.get("A") - v.get("C"))
            return True
        if not v.get("A") and v.get("B") and v.get("C"):
            v.set("A", 180 - v.get("B") - v.get("C"))
            return True
        print("Đã áp dụng công thức tổng 3 góc của tam giác")

    def dieu_tich_tam_giac(self):
        """S = 1/2 * a * ha"""
        v = self.quan_li_do_thi
        s, a, ha = v.get('S'), v.get('a'), v.get('ha')
        
        if a and ha and not s:
            v.set('S', 0.5 * a * ha, "Diện tích cơ bản")
            return True
        if s and a and not ha:
            v.set('ha', (2 * s) / a, "Chiều cao từ diện tích")
            return True
        print("Đã áp dụng công thức diện tích tam giác")

    def pytago(self):
        """Chỉ áp dụng nếu là tam giác vuông (giả sử góc C=90) hoặc biết 2 cạnh"""
        v = self.quan_li_do_thi
        a, b, c = v.get('a'), v.get('b'), v.get('c')
        
        # Nếu biết a, b tính c: c = sqrt(a^2 + b^2)
        if a and b and not c:
            v.set('c', math.sqrt(a**2 + b**2), "Định lý Pytago")
            return True
        print("Đã áp dụng định lý Pytago")

    def dinh_ly_sin(self):
        """a/sinA = 2R"""
        v = self.quan_li_do_thi
        a, A, R = v.get('a'), v.get('A'), v.get('R')
        
        if a and A and not R:
            R_value = a / (2 * math.sin(math.radians(A)))
            v.set('R', R_value, "Định lý Sin")
            return True
        print("Đã áp dụng định lý Sin")
