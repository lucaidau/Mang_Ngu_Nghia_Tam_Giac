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
            self.pytago,
            self.heron,
            self.dinh_ly_sin,
            self.dinh_ly_cos,
            self.chu_vi,
            self.duong_trung_tuyen,
            self.tam_giac_can,
            self.tam_giac_deu,
            
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
            v.them_Doi_Tuong("C", "goc", {"gia_tri": v.get("C"), "cong_thuc": "Tổng 3 góc của tam giác"})
            return True
        if v.get("A") and not v.get("B") and v.get("C"):
            v.set("B", 180 - v.get("A") - v.get("C"))
            v.them_Doi_Tuong("B", "goc", {"gia_tri": v.get("B"), "cong_thuc": "Tổng 3 góc của tam giác"})
            return True
        if not v.get("A") and v.get("B") and v.get("C"):
            v.set("A", 180 - v.get("B") - v.get("C"))
            v.them_Doi_Tuong("A", "goc", {"gia_tri": v.get("A"), "cong_thuc": "Tổng 3 góc của tam giác"})
            return True
        print("Đã áp dụng công thức tổng 3 góc của tam giác")
    
    def chu_vi(self):        
        """Chu vi tam giác: P = a + b + c"""
        v = self.quan_li_do_thi
        a, b, c = v.get('a'), v.get('b'), v.get('c')
        
        if a and b and c and not v.get('P'):
            P_value = a + b + c
            v.set('P', P_value, "Công thức Chu Vi")
            v.them_Doi_Tuong("P", "chu_vi", {"gia_tri": P_value, "cong_thuc": "Công thức Chu Vi"})
            return True
        print("Đã áp dụng công thức Chu Vi")
    
    def heron(self):
        """Diện tích tam giác theo công thức Heron: S = sqrt(p(p-a)(p-b)(p-c)) với p = (a+b+c)/2"""
        v = self.quan_li_do_thi
        a, b, c = v.get('a'), v.get('b'), v.get('c')
        
        if a and b and c and not v.get('S'):
            p = (a + b + c) / 2
            S_value = math.sqrt(p * (p - a) * (p - b) * (p - c))
            v.set('S', S_value, "Công thức Heron")
            v.them_Doi_Tuong("S", "dien_tich", {"gia_tri": S_value, "cong_thuc": "Công thức Heron"})
            return True
        print("Đã áp dụng công thức Heron")

    def pytago(self):
        """Chỉ áp dụng nếu là tam giác vuông (giả sử góc C=90) hoặc biết 2 cạnh"""
        v = self.quan_li_do_thi
        a, b, c = v.get('a'), v.get('b'), v.get('c')
        
        # Nếu biết a, b tính c: c = sqrt(a^2 + b^2)
        if a and b and not c:
            v.set('c', math.sqrt(a**2 + b**2), "Định lý Pytago")
            v.them_Doi_Tuong("c", "canh", {"gia_tri": v.get("c"), "cong_thuc": "Định lý Pytago"})
            return True
        print("Đã áp dụng định lý Pytago")

    def dinh_ly_sin(self):
        """a/sinA = 2R"""
        v = self.quan_li_do_thi
        a, A, R = v.get('a'), v.get('A'), v.get('R')
        
        if a and A and not R:
            R_value = a / (2 * math.sin(math.radians(A)))
            v.set('R', R_value, "Định lý Sin")
            v.them_Doi_Tuong("R", "ban_kinh", {"gia_tri": R_value, "cong_thuc": "Định lý Sin"})
            return True
        print("Đã áp dụng định lý Sin")

    def dinh_ly_cos(self):        
        """a^2 = b^2 + c^2 - 2bc*cosA"""
        v = self.quan_li_do_thi
        a, b, c = v.get('a'), v.get('b'), v.get('c')
        A, B, C = v.get('A'), v.get('B'), v.get('C')

        if a and b and c and not A:
            # Tính góc A từ công thức định lý cosin
            cos_A = (b**2 + c**2 - a**2) / (2 * b * c)
            A_value = math.degrees(math.acos(cos_A))
            v.set('A', A_value, "Định lý Cosin")
            v.them_Doi_Tuong("A", "goc", {"gia_tri": A_value, "cong_thuc": "Định lý Cosin"})
            return True
        if a and b and c and not B:
            # Tính góc B từ công thức định lý cosin
            cos_B = (a**2 + c**2 - b**2) / (2 * a * c)
            B_value = math.degrees(math.acos(cos_B))
            v.set('B', B_value, "Định lý Cosin")
            v.them_Doi_Tuong("B", "goc", {"gia_tri": B_value, "cong_thuc": "Định lý Cosin"})
            return True
        if a and b and c and not C:
            # Tính góc C từ công thức định lý cosin
            cos_C = (a**2 + b**2 - c**2) / (2 * a * b)
            C_value = math.degrees(math.acos(cos_C))
            v.set('C', C_value, "Định lý Cosin")
            v.them_Doi_Tuong("C", "goc", {"gia_tri": C_value, "cong_thuc": "Định lý Cosin"})
            return True
        print("Đã áp dụng định lý Cosin")

    def duong_trung_tuyen(self):
        """Đường trung tuyến: m_a = 0.5 * sqrt(2b^2 + 2c^2 - a^2)"""
        v = self.quan_li_do_thi
        a, b, c = v.get('a'), v.get('b'), v.get('c')
        
        if a and b and c and not v.get('m_a'):
            m_a_value = 0.5 * math.sqrt(2 * b**2 + 2 * c**2 - a**2)
            v.set('m_a', m_a_value, "Công thức Đường Trung Tuyến")
            v.them_Doi_Tuong("m_a", "duong_trung_tuyen", {"gia_tri": m_a_value, "cong_thuc": "Công thức Đường Trung Tuyến"})
            return True
        if a and b and c and not v.get('m_b'):
            m_b_value = 0.5 * math.sqrt(2 * a**2 + 2 * c**2 - b**2)
            v.set('m_b', m_b_value, "Công thức Đường Trung Tuyến")
            v.them_Doi_Tuong("m_b", "duong_trung_tuyen", {"gia_tri": m_b_value, "cong_thuc": "Công thức Đường Trung Tuyến"})
            return True
        if a and b and c and not v.get('m_c'):
            m_c_value = 0.5 * math.sqrt(2 * a**2 + 2 * b**2 - c**2)
            v.set('m_c', m_c_value, "Công thức Đường Trung Tuyến")
            v.them_Doi_Tuong("m_c", "duong_trung_tuyen", {"gia_tri": m_c_value, "cong_thuc": "Công thức Đường Trung Tuyến"})
            return True
        print("Đã áp dụng công thức Đường Trung Tuyến")

    def tam_giac_can(self):
        """Nếu tam giác cân tại A thì a = b và góc A = góc B"""
        v = self.quan_li_do_thi
        a, b, c, A, B, C = v.get('a'), v.get('b'), v.get('c'), v.get('A'), v.get('B'), v.get('C')
        
        if a and b and not A and not B and a == b:
            v.set('A', 180 - 2 * math.degrees(math.acos(a / (2 * a))), "Công thức Tam Giác Cân")
            v.set('B', 180 - 2 * math.degrees(math.acos(a / (2 * a))), "Công thức Tam Giác Cân")
            v.them_Doi_Tuong("A", "goc", {"gia_tri": v.get("A"), "cong_thuc": "Công thức Tam Giác Cân"})
            v.them_Doi_Tuong("B", "goc", {"gia_tri": v.get("B"), "cong_thuc": "Công thức Tam Giác Cân"})
            return True
        if a and c and not A and not C and a == c:
            v.set('A', 180 - 2 * math.degrees(math.acos(a / (2 * a))), "Công thức Tam Giác Cân")
            v.set('C', 180 - 2 * math.degrees(math.acos(a / (2 * a))), "Công thức Tam Giác Cân")
            v.them_Doi_Tuong("A", "goc", {"gia_tri": v.get("A"), "cong_thuc": "Công thức Tam Giác Cân"})
            v.them_Doi_Tuong("C", "goc", {"gia_tri": v.get("C"), "cong_thuc": "Công thức Tam Giác Cân"})
            return True
        if b and c and not B and not C and b == c:
            v.set('B', 180 - 2 * math.degrees(math.acos(b / (2 * b))), "Công thức Tam Giác Cân")
            v.set('C', 180 - 2 * math.degrees(math.acos(b / (2 * b))), "Công thức Tam Giác Cân")
            v.them_Doi_Tuong("B", "goc", {"gia_tri": v.get("B"), "cong_thuc": "Công thức Tam Giác Cân"})
            v.them_Doi_Tuong("C", "goc", {"gia_tri": v.get("C"), "cong_thuc": "Công thức Tam Giác Cân"})
            return True
        print("Đã áp dụng công thức Tam Giác Cân")
    