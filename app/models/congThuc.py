import math
import networkx as nx
from .quanLiDoThi import QuanLiDoThi

class Rules:
    def __init__(self, qldt: QuanLiDoThi):
        self.quan_li_do_thi = qldt
        self.list_rules = [
            self.tong3goc,
            self.pytago,
            self.heron,
            self.dinh_ly_sin,
            self.dinh_ly_cos,
            self.chu_vi,
            self.duong_trung_tuyen,
            self.tam_giac_can,
            self.tam_giac_deu,
            self.dien_tich_sin_goc,
            self.dien_tich_ngoai_tiep,
            self.dien_tich_noi_tiep,
            self.duong_cao,
            self.duong_phan_giac,
            self.ti_le_phan_giac,
            self.check_tam_giac_vuong,
            self.he_thuc_luong,
            self.r_ngoai_tiep_vuong,
            self.kiem_tra_hop_le,
            self.tinh_goc_tu_3_canh,
            # Thêm các công thức khác vào đây  
        ]

    def execute_alt(self):
        has_changed = True

        while has_changed:
            so_not_cu = len(self.quan_li_do_thi.lay_do_thi().nodes)
            so_canh_cu = len(self.quan_li_do_thi.lay_do_thi().edges)
 
            for rule in self.list_rules:
                if rule(): # Thêm dấu () để thực thi hàm
                    has_changed = True 

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
        v = self.quan_li_do_thi
        changed = False
    
        # Giả sử trong dữ liệu có thuộc tính 'dinh_can'
        dinh = v.get('dinh_can') 
    
        if dinh == 'A':
            # Hệ quả 1: Cạnh b = c
            if v.get('b') and not v.get('c'):
                v.set('c', v.get('b'))
                changed = True
            elif v.get('c') and not v.get('b'):
                v.set('b', v.get('c'))
                changed = True
            
        # Hệ quả 2: Góc B = Góc C
            if v.get('B') and not v.get('C'):
                v.set('C', v.get('B'))
                changed = True
            elif v.get('C') and not v.get('B'):
                v.set('B', v.get('C'))
                changed = True
        elif dinh == 'B':
            # Hệ quả 1: Cạnh a = c
            if v.get('a') and not v.get('c'):
                v.set('c', v.get('a'))
                changed = True
            elif v.get('c') and not v.get('a'):
                v.set('a', v.get('c'))
                changed = True
            # Hệ quả 2: Góc A = Góc C
            if v.get('A') and not v.get('C'):
                v.set('C', v.get('A'))
                changed = True
            elif v.get('C') and not v.get('A'):
                v.set('A', v.get('C'))
                changed = True
        elif dinh == 'C':
            # Hệ quả 1: Cạnh a = b
            if v.get('a') and not v.get('b'):
                v.set('b', v.get('a'))
                changed = True
            elif v.get('b') and not v.get('a'):
                v.set('a', v.get('b'))
                changed = True
            # Hệ quả 2: Góc A = Góc B
            if v.get('A') and not v.get('B'):
                v.set('B', v.get('A'))
                changed = True
            elif v.get('B') and not v.get('A'):
                v.set('A', v.get('B'))
                changed = True

    def tam_giac_deu(self):
        v = self.quan_li_do_thi
        changed = False
    
        for goc in ['A', 'B', 'C']:
            if not v.get(goc):
                v.set(goc, 60)
                v.them_Doi_Tuong(goc, "goc", {"gia_tri": 60, "cong_thuc": "Tính chất tam giác đều"})
                changed = True
            
        canh_da_biet = v.get('a') or v.get('b') or v.get('c')
        if canh_da_biet:
            for c in ['a', 'b', 'c']:
                if not v.get(c):
                    v.set(c, canh_da_biet)
                    v.them_Doi_Tuong(c, "canh", {"gia_tri": canh_da_biet, "cong_thuc": "Tính chất tam giác đều"})
                    changed = True
                
    # Diện tích qua bán kính đường tròn ngoại tiếp R: S = (abc) / (4R)
    def dien_tich_ngoai_tiep(self):
        v = self.quan_li_do_thi
        a, b, c, S, R = v.get('a'), v.get('b'), v.get('c'), v.get('S'), v.get('R')
        if a and b and c and S and not R:
            R_val = (a * b * c) / (4 * S)
            v.set('R', R_val)
            v.them_Doi_Tuong("R", "ban_kinh_ngoai", {"gia_tri": R_val, "cong_thuc": "S = abc/4R"})
            return True
        if a and b and c and R and not S:
            S_val = (a * b * c) / (4 * R)
            v.set('S', S_val)
            v.them_Doi_Tuong("S", "dien_tich", {"gia_tri": S_val, "cong_thuc": "S = abc/4R"})
            return True

    # Diện tích qua bán kính nội tiếp r: S = p * r
    def dien_tich_noi_tiep(self):
        v = self.quan_li_do_thi
        a, b, c, S, r = v.get('a'), v.get('b'), v.get('c'), v.get('S'), v.get('r')
        if a and b and c:
            p = (a + b + c) / 2
            if not S and r:
                S_val = p * r
                v.set('S', S_val)
                v.them_Doi_Tuong("S", "dien_tich", {"gia_tri": S_val, "cong_thuc": "S = p*r"})
                return True
            if S and not r:
                r_val = S / p
                v.set('r', r_val)
                v.them_Doi_Tuong("r", "ban_kinh_noi", {"gia_tri": r_val, "cong_thuc": "S = p*r"})
                return True

    # Diện tích qua 2 cạnh và góc xen giữa: S = 0.5 * a * b * sin(C)
    def dien_tich_sin_goc(self):
        v = self.quan_li_do_thi
        a, b, C_deg, S = v.get('a'), v.get('b'), v.get('C'), v.get('S')
        if a and b and C_deg and not S:
            S_val = 0.5 * a * b * math.sin(math.radians(C_deg))
            v.set('S', S_val)
            v.them_Doi_Tuong("S", "dien_tich", {"gia_tri": S_val, "cong_thuc": "S = 1/2*ab*sinC"})
            return True

    # Đường cao: h_a = 2S / a
    def duong_cao(self):
        v = self.quan_li_do_thi
        a, S, ha = v.get('a'), v.get('S'), v.get('h_a')
        if a and S and not ha:
            ha_val = (2 * S) / a
            v.set('h_a', ha_val)
            v.them_Doi_Tuong("h_a", "duong_cao", {"gia_tri": ha_val, "cong_thuc": "h = 2S/a"})
            return True

    # Đường phân giác trong: l_a = (2bc * cos(A/2)) / (b+c)
    def duong_phan_giac(self):
        v = self.quan_li_do_thi
        b, c, A_deg, la = v.get('b'), v.get('c'), v.get('A'), v.get('l_a')
        if b and c and A_deg and not la:
            la_val = (2 * b * c * math.cos(math.radians(A_deg / 2))) / (b + c)
            v.set('l_a', la_val)
            v.them_Doi_Tuong("l_a", "phan_giac", {"gia_tri": la_val, "cong_thuc": "Công thức phân giác"})
            return True

    # Tính chất đường phân giác (tỉ lệ đoạn thẳng trên cạnh đáy d_b, d_c)
    def ti_le_phan_giac(self):
        v = self.quan_li_do_thi
        a, b, c = v.get('a'), v.get('b'), v.get('c')
        db, dc = v.get('d_b'), v.get('d_c') # d_b, d_c là đoạn BD, DC trên cạnh BC
        if b and c and a and not db and not dc:
            db_val = (c * a) / (b + c)
            dc_val = a - db_val
            v.set('d_b', db_val); v.set('d_c', dc_val)
            return True

    # Nhận biết tam giác vuông qua Pytago đảo
    def check_tam_giac_vuong(self):
        v = self.quan_li_do_thi
        a, b, c = v.get('a'), v.get('b'), v.get('c')
        if a and b and c and not v.get('loai_vuong'):
            if math.isclose(a**2 + b**2, c**2):
                v.set('loai_vuong', 'C'); return True
            if math.isclose(a**2 + c**2, b**2):
                v.set('loai_vuong', 'B'); return True
            if math.isclose(b**2 + c**2, a**2):
                v.set('loai_vuong', 'A'); return True

    # Hệ thức lượng trong tam giác vuông (AH^2 = BH * CH)
    def he_thuc_luong(self):
        v = self.quan_li_do_thi
        h, bh, ch = v.get('h_a'), v.get('BH'), v.get('CH')
        if v.get('loai_vuong') == 'A':
            if bh and ch and not h:
                h_val = math.sqrt(bh * ch)
                v.set('h_a', h_val); return True

    # Bán kính ngoại tiếp tam giác vuông (R = huyền / 2)
    def r_ngoai_tiep_vuong(self):
        v = self.quan_li_do_thi
        if v.get('loai_vuong') == 'A' and v.get('a') and not v.get('R'):
            v.set('R', v.get('a') / 2); return True

    # Kiểm tra bất đẳng thức tam giác (Để validate dữ liệu)
    def kiem_tra_hop_le(self):
        v = self.quan_li_do_thi
        a, b, c = v.get('a'), v.get('b'), v.get('c')
        if a and b and c:
            if not (a + b > c and a + c > b and b + c > a):
                print("Dữ liệu tam giác không hợp lệ!")
                return False

    # Định lý Cosin tính góc (Dành riêng cho việc tìm góc khi biết 3 cạnh)
    def tinh_goc_tu_3_canh(self):
        v = self.quan_li_do_thi
        a, b, c = v.get('a'), v.get('b'), v.get('c')
        if a and b and c:
            changed = False
            if not v.get('A'):
                v.set('A', math.degrees(math.acos((b**2 + c**2 - a**2)/(2*b*c))))
                changed = True
            if not v.get('B'):
                v.set('B', math.degrees(math.acos((a**2 + c**2 - b**2)/(2*a*c))))
                changed = True
            return changed