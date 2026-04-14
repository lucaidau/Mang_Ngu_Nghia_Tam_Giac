import math
from .quanLiDoThi import QuanLiDoThi
import math


class Rules:
    def __init__(self, qldt: QuanLiDoThi):
        self.quan_li_do_thi = qldt
        self.error = []
        self.a = self.b = self.c = None
        self.A = self.B = self.C = None
        self.S = self.p = self.P = self.R = self.r = None
        self.ha = self.hb = self.hc = None
        self.la = self.lb = self.lc = None

        self.is_vuong = False
        self.is_can = False
        self.is_deu = False
        self.is_tu = False
        self.is_nhon = False
        self.dinh_can = None

    def _sync_from_graph(self):
        v = self.quan_li_do_thi
        self.a, self.b, self.c = v.get("a"), v.get("b"), v.get("c")
        self.A, self.B, self.C = v.get("A"), v.get("B"), v.get("C")
        self.S, self.P, self.R, self.r = v.get("S"), v.get("P"), v.get("R"), v.get("r")
        self.ha, self.hb, self.hc = v.get("h_a"), v.get("h_b"), v.get("h_c")
        self.la, self.lb, self.lc = v.get("l_a"), v.get("l_b"), v.get("l_c")
    
    def _save(self, key, loai, value, method_name):
        if value is not None:
            float_value = float(value)
            setattr(self, key, float_value) 
            self.quan_li_do_thi.set(key, float_value, method_name)
            info = {
            "gia_tri":round(float_value,2),
            "tu_cong_thuc": method_name
            }
            self.quan_li_do_thi.them_Doi_Tuong(key, loai, info)
        
        if self.a and self.b and self.c:
            self.p = (self.a + self.b + self.c) / 2
        if self.P and not self.p:
            self.p = self.P / 2
        elif self.p and not self.P:
            self.P = self.p * 2

        print(f" -> Đã tính được {key} = {float_value:2f} bằng {method_name}")

    def execute_alt(self):
        if not self.kiem_tra_bat_dang_thuc_tam_giac():
            self.error.append("Vi phạm bất đẳng thức tam giác hoặc dữ liệu lỗi.")
            return
        
        has_changed = True
        while has_changed:
            self._sync_from_graph()

            so_not_cu = len(self.quan_li_do_thi.lay_do_thi().nodes)
            so_canh_cu = len(self.quan_li_do_thi.lay_do_thi().edges)

            self.tam_giac_can()
            self.tam_giac_vuong_can()
            self.tam_giac_deu()
            self.tam_giac_tu_nhon()

            self.tong3goc()
            self.chu_vi()
            self.heron()
            self.pytago()
            self.dinh_ly_sin()
            self.dinh_ly_cos()
            self.duong_trung_tuyen()

            self.dien_tich_ngoai_tiep()
            self.dien_tich_noi_tiep()
            self.dien_tich_sin_goc()
            self.duong_cao()
            self.duong_phan_giac()
            self.ti_le_phan_giac()
            self.tam_ngoai_tiep()
            self.tam_noi_tiep()

            self._sync_from_graph()
            # Thêm các công thức khác vào đây

            so_not_moi = len(self.quan_li_do_thi.lay_do_thi().nodes)
            so_canh_moi = len(self.quan_li_do_thi.lay_do_thi().edges)

            if so_not_cu == so_not_moi and so_canh_cu == so_canh_moi:
                has_changed = False

    """Các luật và công thức"""
    def kiem_tra_bat_dang_thuc_tam_giac(self):
        v = self.quan_li_do_thi

        if self.a and self.b and self.c:
            if not (self.a + self.b > self.c and self.a + self.c > self.b and self.b + self.c > self.a):
                self.errors.append(f"Vi phạm bất đẳng thức tam giác: {self.a}, {self.b}, {self.c} không thể tạo thành tam giác.")
                return False
        return True
    
    def tam_giac_can(self):
        """Chứng minh và kích hoạt dữ liệu tam giác cân"""
        # Trường hợp 1: Nếu người dùng nhập vào là tam giác cân tại A
        if self.dinh_can == "A" or (self.B and self.C and math.isclose(self.B, self.C)):
            self.is_can = True
            changed = False
            
            # TỪ CHỨNG MINH -> SUY RA DỮ LIỆU TÍNH TOÁN
            if self.b and not self.c:
                self._save("c", "canh", self.b, "Tính chất tam giác cân tại A (b=c)")
                changed = True
            elif self.c and not self.b:
                self._save("b", "canh", self.c, "Tính chất tam giác cân tại A (c=b)")
                changed = True
                
            if self.B and not self.C:
                self._save("C", "goc", self.B, "Tính chất tam giác cân tại A (B=C)")
                changed = True
            return changed
        
        # Trường hợp 2: Nếu người dùng nhập vào là tam giác cân tại B
        if self.dinh_can == "B" or (self.A and self.C and math.isclose(self.A, self.C)):
            self.is_can = True
            changed = False
            
            if self.a and not self.c:
                self._save("c", "canh", self.a, "Tính chất tam giác cân tại B (a=c)")
                changed = True
            elif self.c and not self.a:
                self._save("a", "canh", self.c, "Tính chất tam giác cân tại B (c=a)")
                changed = True
                
            if self.A and not self.C:
                self._save("C", "goc", self.A, "Tính chất tam giác cân tại B (A=C)")
                changed = True
            return changed
        
        # Trường hợp 3: Nếu người dùng nhập vào là tam giác cân tại C
        if self.dinh_can == "C" or (self.A and self.B and math.isclose(self.A, self.B)):
            self.is_can = True
            changed = False
            
            if self.a and not self.b:
                self._save("b", "canh", self.a, "Tính chất tam giác cân tại C (a=b)")
                changed = True
            elif self.b and not self.a:
                self._save("a", "canh", self.b, "Tính chất tam giác cân tại C (b=a)")
                changed = True
                
            if self.A and not self.B:
                self._save("B", "goc", self.A, "Tính chất tam giác cân tại C (A=B)")
                changed = True
            return changed
        
        return False

    def tam_giac_deu(self):
        """Chứng minh và suy luận tam giác đều"""
        # Dấu hiệu: 3 cạnh bằng nhau OR 3 góc bằng nhau OR (Cân + 1 góc 60 độ)
        is_deu_sign = False
        if self.a and self.b and self.c and math.isclose(self.a, self.b) and math.isclose(self.b, self.c):
            is_deu_sign = True
        elif self.A and self.B and self.C and math.isclose(self.A, 60) and math.isclose(self.B, 60):
            is_deu_sign = True
        elif self.is_can and (math.isclose(self.A or 0, 60) or math.isclose(self.B or 0, 60) or math.isclose(self.C or 0, 60)):
            is_deu_sign = True

        if is_deu_sign:
            self.is_deu = True
            # 1. Điền tất cả các góc bằng 60
            for g in ["A", "B", "C"]:
                if not getattr(self, g):
                    self._save(g, "goc", 60, "Tính chất tam giác đều")
            
            # 2. Điền tất cả các cạnh bằng nhau
            canh_chuan = self.a or self.b or self.c
            if canh_chuan:
                for c in ["a", "b", "c"]:
                    if not getattr(self, c):
                        self._save(c, "canh", canh_chuan, "Tính chất tam giác đều")
            return True
        return False

    def tam_giac_tu_nhon(self):
        v = self.quan_li_do_thi

        if self.a and self.b and self.c:
            sides = sorted([self.a, self.b, self.c])
            a2, b2, c2 = sides[0]**2, sides[1]**2, sides[2]**2
            
            if math.isclose(a2 + b2, c2):
                self.is_vuong = True
            elif a2 + b2 < c2:
                self.is_tu = True
                self._save("loai_goc", "tinh_chat", self.is_tu, "Tam giác tù")
            else:
                self.is_tu = False
                self._save("loai_goc", "tinh_chat", self.is_tu, "Tam giác nhọn")
            
    def tam_giac_vuong_can(self):
        """Suy luận đặc thù cho tam giác vuông cân"""
        # Dấu hiệu: (Vuông + Cân tại cùng 1 đỉnh) OR (Vuông + 1 góc 45 độ)
        if self.is_vuong and (self.is_can or self.A == 45 or self.B == 45 or self.C == 45):
            # Giả sử vuông cân tại A
            if self.dinh_vuong == "A":
                # 1. Suy ra góc
                if not self.B: self._save("B", "goc", 45, "Tính chất vuông cân")
                if not self.C: self._save("C", "goc", 45, "Tính chất vuông cân")
                # 2. Suy ra cạnh
                if self.b and not self.c: self._save("c", "canh", self.b, "Vuông cân tại A (b=c)")
                if self.b and not self.a: self._save("a", "canh", self.b * math.sqrt(2), "Cạnh huyền = c.sqrt(2)")
                if self.a and not self.b: self._save("b", "canh", self.a / math.sqrt(2), "Cạnh góc vuông = a/sqrt(2)")
                return True
        return False
    
    def tam_giac_vuong(self):
        """Chứng minh và kích hoạt hệ thức lượng tam giác vuông"""
        # Dấu hiệu: 1 góc = 90 hoặc thỏa mãn Pytago
        if self.A == 90: self.is_vuong = True; self.dinh_vuong = "A"
        elif self.B == 90: self.is_vuong = True; self.dinh_vuong = "B"
        elif self.C == 90: self.is_vuong = True; self.dinh_vuong = "C"
        
        # Nếu chưa có góc nhưng thỏa mãn a^2 + b^2 = c^2 (đảo)
        if not self.is_vuong and self.a and self.b and self.c:
            sides = sorted([self.a, self.b, self.c])
            if math.isclose(sides[0]**2 + sides[1]**2, sides[2]**2):
                self.is_vuong = True
                # Xác định đỉnh vuông là đối diện cạnh lớn nhất
                max_side = max(self.a, self.b, self.c)
                if max_side == self.a: self.dinh_vuong = "A"; self._save("A", "goc", 90, "Pytago đảo")
                elif max_side == self.b: self.dinh_vuong = "B"; self._save("B", "goc", 90, "Pytago đảo")
                else: self.dinh_vuong = "C"; self._save("C", "goc", 90, "Pytago đảo")

        # KÍCH HOẠT TÍNH TOÁN: Nếu đã biết là vuông tại đâu, tính cạnh thiếu ngay
        if self.is_vuong:
            if self.dinh_vuong == "A": # Vuông tại A -> a là cạnh huyền
                if self.b and self.c and not self.a: return self._save("a", "canh", math.sqrt(self.b**2 + self.c**2), "Pytago")
                if self.a and self.b and not self.c: return self._save("c", "canh", math.sqrt(self.a**2 - self.b**2), "Pytago")
                if self.a and self.c and not self.b: return self._save("b", "canh", math.sqrt(self.a**2 - self.c**2), "Pytago")
        return False

    def tong3goc(self):
        """A + B + C = 180 độ"""
        v = self.quan_li_do_thi

        if self.A and self.B and not self.C:
            return self._save("C", "goc", 180 - self.A - self.B, "Tổng 3 góc")
            
        if self.A and self.C and not self.B:
            return self._save("B", "goc", 180 - self.A - self.C, "Tổng 3 góc")
            
        if self.B and self.C and not self.A:
            return self._save("A", "goc", 180 - self.B - self.C, "Tổng 3 góc")
        
        print("Đã áp dụng công thức tổng 3 góc của tam giác")
        return False

    def chu_vi(self):
        """Chu vi tam giác"""
        v = self.quan_li_do_thi

        if self.a and self.b and self.c and not v.get("P"):
            return self._save("P","chu_vi", self.a + self.b + self.c, "Chu vi từ S và r")
        if self.S and self.r and not self.P:
            return self._save("P", "chu_vi", (2 * self.S) / self.r, "Chu vi từ S và r")
        if self.R and self.A and self.B and self.C and not self.P:
            return self._save("P", "chu_vi", 2 * self.R * (math.sin(math.radians(self.A)) + 
                               math.sin(math.radians(self.B)) + 
                               math.sin(math.radians(self.C))), "Chu vi từ R và 3 góc")
        print("Đã áp dụng công thức Chu Vi")
        return False

    def heron(self):
        """Diện tích tam giác theo công thức Heron"""
        v = self.quan_li_do_thi

        if self.a and self.b and self.c and not v.get("S"):
            p = (self.a + self.b + self.c) / 2
            S_value = math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))
            return self._save("S","dien_tich", S_value, "Diện tích từ công thức Heron")
        print("Đã áp dụng công thức Heron")

    def pytago(self):
        """Chỉ áp dụng nếu là tam giác vuông (giả sử góc C=90) hoặc biết 2 cạnh"""
        v = self.quan_li_do_thi
        # Nếu biết a, b tính c: c = sqrt(a^2 + b^2)
        if self.a and self.b and not self.c:
            S_value = math.sqrt(self.a**2 + self.b**2)
            return self._save("c", "canh", S_value, "Pytago")
        
        # Nếu biết a, c tính b: b = sqrt(c^2 - a^2)
        if self.a and self.c and not self.b:
            if self.c > self.a:  # Đảm bảo c là cạnh huyền
                S_value = math.sqrt(self.c**2 - self.a**2)
                return self._save("b", "canh", S_value, "Pytago")
            
        # Nếu biết b, c tính a: a = sqrt(c^2 - b^2)
        if self.b and self.c and not self.a:
            if self.c > self.b:  # Đảm bảo c là cạnh huyền
                S_value = math.sqrt(self.c**2 - self.b**2)
                return self._save("a", "canh", S_value, "Pytago")
        print("Đã áp dụng định lý Pytago")

    def dinh_ly_sin(self):
        """a/sinA = 2R"""
        v = self.quan_li_do_thi

        if self.a and self.A and not self.R:
            R_value = self.a / (2 * math.sin(math.radians(self.A)))
            return self._save("R", "ban_kinh", R_value, "Định lý Sin")
        if self.b and self.B and not self.R:
            R_value = self.b / (2 * math.sin(math.radians(self.B)))
            return self._save("R", "ban_kinh", R_value, "Định lý Sin")
        if self.c and self.C and not self.R:
            R_value = self.c / (2 * math.sin(math.radians(self.C)))
            return self._save("R", "ban_kinh", R_value, "Định lý Sin")
        print("Đã áp dụng định lý Sin")

    def dinh_ly_cos(self):
        v = self.quan_li_do_thi
        if self.a and self.b and self.c and not self.A:
            # Tính góc A từ công thức định lý cosin
            cos_A = (self.b**2 + self.c**2 - self.a**2) / (2 * self.b * self.c)
            A_value = math.degrees(math.acos(cos_A))
            return self._save("A", "goc", A_value, "Định lý Cosin")
        if self.a and self.b and self.c and not self.B:
            # Tính góc B từ công thức định lý cosin
            cos_B = (self.a**2 + self.c**2 - self.b**2) / (2 * self.a * self.c) 
            B_value = math.degrees(math.acos(cos_B))
            return self._save("B", "goc", B_value, "Định lý Cosin")
        if self.a and self.b and self.c and not self.C:
            # Tính góc C từ công thức định lý cosin
            cos_C = (self.a**2 + self.b**2 - self.c**2) / (2 * self.a * self.b)
            C_value = math.degrees(math.acos(cos_C))
            v.set("C", C_value, "Định lý Cosin")
            v.them_Doi_Tuong(
                "C", "goc", {"gia_tri": C_value, "cong_thuc": "Định lý Cosin"}
            )
            return True
        print("Đã áp dụng định lý Cosin")

    def duong_trung_tuyen(self):
        """Đường trung tuyến: m_a = 0.5 * sqrt(2b^2 + 2c^2 - a^2)"""
        v = self.quan_li_do_thi

        if self.a and self.b and self.c and not v.get("m_a"):
            m_a_value = 0.5 * math.sqrt(2 * self.b**2 + 2 * self.c**2 - self.a**2)
            return self._save("m_a", "duong_trung_tuyen", m_a_value, "Công thức Đường Trung Tuyến")
        if self.a and self.b and self.c and not v.get("m_b"):
            m_b_value = 0.5 * math.sqrt(2 * self.a**2 + 2 * self.c**2 - self.b**2)
            return self._save("m_b", "duong_trung_tuyen", m_b_value, "Công thức Đường Trung Tuyến")
        if self.a and self.b and self.c and not v.get("m_c"):
            m_c_value = 0.5 * math.sqrt(2 * self.a**2 + 2 * self.b**2 - self.c**2)
            return self._save("m_c", "duong_trung_tuyen", m_c_value, "Công thức Đường Trung Tuyến")
        print("Đã áp dụng công thức Đường Trung Tuyến")

    # Diện tích qua bán kính đường tròn ngoại tiếp R: S = (abc) / (4R)
    def dien_tich_ngoai_tiep(self):
        v = self.quan_li_do_thi

        if self.a and self.b and self.c and self.S and not self.R:
            R_val = (self.a * self.b * self.c) / (4 * self.S)
            return self._save("R", "ban_kinh", R_val, "Công thức diện tích ngoại tiếp")
        if self.a and self.b and self.c and self.R and not self.S:
            S_val = (self.a * self.b * self.c) / (4 * self.R)
            return self._save("S", "dien_tich", S_val, "Công thức diện tích ngoại tiếp")
        print("Đã áp dụng công thức diện tích ngoại tiếp")

    # Diện tích qua bán kính nội tiếp r: S = p * r
    def dien_tich_noi_tiep(self):
        v = self.quan_li_do_thi
        
        if self.a and self.b and self.c:
            p = (self.a + self.b + self.c) / 2
            if not self.S and self.r:
                S_val = p * self.r
                return self._save("S", "dien_tich", S_val, "S = p*r")
            if self.S and not self.r:
                r_val = self.S / p
                return self._save("r", "ban_kinh_noi_tiep", r_val, "r = S/p")
        print("Đã áp dụng công thức diện tích nội tiếp")

    # Diện tích qua 2 cạnh và góc xen giữa: S = 0.5 * a * b * sin(C)
    def dien_tich_sin_goc(self):
        v = self.quan_li_do_thi

        if self.a and self.b and self.C and not self.S:
            S_val = 0.5 * self.a * self.b * math.sin(math.radians(self.C))
            return self._save("S", "dien_tich", S_val, "S = 1/2*ab*sinC")
        # 2. Trường hợp biết cạnh b, c và góc A (Tăng tính liên kết)
        if self.b and self.c and self.A and not self.S:  
            S_val = 0.5 * self.b * self.c * math.sin(math.radians(self.A))
            return self._save("S", "dien_tich", S_val, "S = 1/2 * b * c * sin(A)")
        # 3. Trường hợp biết cạnh a, c và góc B
        if self.a and self.c and self.B and not self.S:
            S_val = 0.5 * self.a * self.c * math.sin(math.radians(self.B))
            return self._save("S", "dien_tich", S_val, "S = 1/2 * a * c * sin(B)")
        print("Đã áp dụng công thức diện tích sin góc")

    def duong_cao(self):
        """Đường cao: h = 2S / cạnh_tương_ứng"""
        # 1. Tính h_a
        if self.S and self.a and not self.ha:
            val = (2 * self.S) / self.a
            return self._save("ha", "duong_cao", val, "h_a = 2S / a")

        # 2. Tính h_b
        if self.S and self.b and not self.hb:
            val = (2 * self.S) / self.b
            return self._save("hb", "duong_cao", val, "h_b = 2S / b")

        # 3. Tính h_c
        if self.S and self.c and not self.hc:
            val = (2 * self.S) / self.c
            return self._save("hc", "duong_cao", val, "h_c = 2S / c")

        return False

    # Đường phân giác trong: l_a = (2bc * cos(A/2)) / (b+c)
    def duong_phan_giac(self):
        v = self.quan_li_do_thi

        if self.b and self.c and self.A and not self.la:
            la_val = (2 * self.b * self.c * math.cos(math.radians(self.A / 2))) / (self.b + self.c)
            return self._save("l_a", "phan_giac", la_val, "Công thức phân giác")
        if self.a and self.c and self.B and not self.lb:
            lb_val = (2 * self.a * self.c * math.cos(math.radians(self.B / 2))) / (self.a + self.c)
            return self._save("l_b", "phan_giac", lb_val, "Công thức phân giác")
        if self.a and self.b and self.C and not self.lc:
            lc_val = (2 * self.a * self.b * math.cos(math.radians(self.C / 2))) / (self.a + self.b)
            return self._save("l_c", "phan_giac", lc_val, "Công thức phân giác")
        print("Đã áp dụng công thức đường phân giác")

    # Tính chất đường phân giác (tỉ lệ đoạn thẳng trên cạnh đáy d_b, d_c)
    def ti_le_phan_giac(self):
        v = self.quan_li_do_thi

        db, dc = v.get("d_b"), v.get("d_c")  # d_b, d_c là đoạn BD, DC trên cạnh BC
        if self.b and self.c and self.a and not db and not dc:
            db_val = (self.c * self.a) / (self.b + self.c)
            dc_val = self.a - db_val
            v.set("d_b", db_val)
            v.set("d_c", dc_val)
            return True
        print("Đã áp dụng công thức Tam Giác Cân")

    def tam_ngoai_tiep(self):
        v = self.quan_li_do_thi
        # Lấy tọa độ 3 điểm (giả sử lưu dạng tuple (x, y))
        pA, pB, pC = v.get('posA'), v.get('posB'), v.get('posC')
        
        if pA and pB and pC and not v.get('posO'):
            x1, y1 = pA; x2, y2 = pB; x3, y3 = pC
            D = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
            if D == 0: return False # 3 điểm thẳng hàng
            
            ux = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / D
            uy = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / D
            
            v.set('posO', (ux, uy), "Công thức tọa độ tâm ngoại tiếp")
            return True
        return False
    
    def tam_noi_tiep(self):
        v = self.quan_li_do_thi
        pA, pB, pC = v.get('posA'), v.get('posB'), v.get('posC')
        
        # Cần cả tọa độ 3 đỉnh và độ dài 3 cạnh
        if all([pA, pB, pC, self.a, self.b, self.c]) and not v.get('posI'):
            chu_vi = self.a + self.b + self.c
            ix = (self.a * pA[0] + self.b * pB[0] + self.c * pC[0]) / chu_vi
            iy = (self.a * pA[1] + self.b * pB[1] + self.c * pC[1]) / chu_vi
            
            v.set('posI', (ix, iy), "Công thức tọa độ tâm nội tiếp")
            return True
        return False