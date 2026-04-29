import math
from collections import deque
from typing import Callable, Any, Dict, List, Tuple, Optional, Union
from .quanLiDoThi import QuanLiDoThi

class Rules:
    def __init__(self, qldt: QuanLiDoThi):

        self.quan_li_do_thi: QuanLiDoThi = qldt
        self.error: List[str] = []
        
        self.a: Optional[float] = None
        self.b: Optional[float] = None
        self.c: Optional[float] = None
        self.A: Optional[float] = None
        self.B: Optional[float] = None
        self.C: Optional[float] = None
        self.S: Optional[float] = None
        self.p: Optional[float] = None
        self.P: Optional[float] = None
        self.R: Optional[float] = None
        self.r: Optional[float] = None
        self.d_a: Optional[float] = None
        self.d_b: Optional[float] = None
        self.d_c: Optional[float] = None
        self.h_a: Optional[float] = None
        self.h_b: Optional[float] = None
        self.h_c: Optional[float] = None
        self.l_a: Optional[float] = None
        self.l_b: Optional[float] = None
        self.l_c: Optional[float] = None
        self.m_a: Optional[float] = None
        self.m_b: Optional[float] = None
        self.m_c: Optional[float] = None
        self.posA: Optional[Tuple[float, float]] = None
        self.posB: Optional[Tuple[float, float]] = None
        self.posC: Optional[Tuple[float, float]] = None
        self.posO: Optional[Tuple[float, float]] = None
        self.posI: Optional[Tuple[float, float]] = None

        self.is_vuong: bool = False
        self.is_can: bool = False
        self.is_deu: bool = False
        self.is_tu: bool = False
        self.is_nhon: bool = False
        self.dinh_can: Optional[str] = None
        self.dinh_vuong: Optional[str] = None

        self.changed: bool = False
        self.debug: bool = False

        self.trace: List[str] = []
        self.cache: set[tuple[str, tuple[float, ...]]] = set() 
        self.new_values: set[str] = set()  
        self.is_valid: bool = True

        # Nhóm hàm dùng chung cho cả 3 góc a, b, c
        common_canh: list[Callable[[], bool | None]] = [
            self.pytago, self.heron, self.dinh_ly_sin, self.dinh_ly_cos, 
            self.chu_vi, self.duong_trung_tuyen, self.duong_cao, 
            self.duong_phan_giac, self.dien_tich_ngoai_tiep, 
            self.dien_tich_noi_tiep, self.ti_le_phan_giac
        ]
        
        # Nhóm hàm dùng chung cho cả 3 góc A, B, C
        common_goc: list[Callable[[], bool | None]] = [
            self.tong3goc, self.dinh_ly_sin, self.dinh_ly_cos, 
            self.dien_tich_sin_goc, self.duong_phan_giac
        ]

        self.dependency_map: dict[str, list[Callable[[], bool | None]]] = {}

        for k in ["a", "b", "c"]:
            self.dependency_map[k] = common_canh.copy()

        for k in ["A", "B", "C"]:
            self.dependency_map[k] = common_goc.copy()

        self.dependency_map.update({
            "S": [self.duong_cao, self.dien_tich_ngoai_tiep, self.dien_tich_noi_tiep, self.dien_tich_sin_goc],
            "P": [self.heron, self.dien_tich_noi_tiep, self.chu_vi],
            "p": [self.heron, self.dien_tich_noi_tiep], # Nửa chu vi kích hoạt Heron
            "R": [self.dinh_ly_sin, self.dien_tich_ngoai_tiep, self.chu_vi],
            "r": [self.dien_tich_noi_tiep, self.chu_vi],
            
            # Kích hoạt nhóm tính tọa độ tâm
            "posA": [self.tam_ngoai_tiep, self.tam_noi_tiep],
            "posB": [self.tam_ngoai_tiep, self.tam_noi_tiep],
            "posC": [self.tam_ngoai_tiep, self.tam_noi_tiep],
            
            # Các biến hệ quả (để nếu tính được cái này có thể tính tiếp cái kia)
            "h_a": [self.duong_cao],
            "h_b": [self.duong_cao],
            "h_c": [self.duong_cao],
            "l_a": [self.duong_phan_giac],
            "l_b": [self.duong_phan_giac],
            "l_c": [self.duong_phan_giac],
        })

    def _has(self, *keys: str) -> bool:
        return all(getattr(self, key, None) is not None for key in keys)
    
    def _sync_from_graph(self) -> None:
        v = self.quan_li_do_thi

        def get_val(key):
            val = v.get(key)
            return val if (val is not None and val != 0) else None
        
        self.a, self.b, self.c = get_val("a"), get_val("b"), get_val("c")
        self.A, self.B, self.C = get_val("A"), get_val("B"), get_val("C")
        self.S, self.P, self.R, self.r = get_val("S"), get_val("P"), get_val("R"), get_val("r")
        self.h_a, self.h_b, self.h_c = get_val("h_a"), get_val("h_b"), get_val("h_c")
        self.l_a, self.l_b, self.l_c = get_val("l_a"), get_val("l_b"), get_val("l_c")
        if self.P: self.p = self.P / 2
    
    def get(self, ten_doi_tuong):
        if self.quan_li_do_thi.G.has_node(ten_doi_tuong):
            return self.quan_li_do_thi.G.nodes[ten_doi_tuong].get("gia_tri")
        return None  # Sửa từ 0 thành None
    
    def _save(self, key: str, loai: str, value: Union[float, Tuple[float, ...], None], method_name: str, tu_cac_bien: Optional[List[str]] = None) -> bool:
        if value is None or not self.is_valid: return False
        
        final_value: Union[float, Tuple[float, ...]] = value if isinstance(value, tuple) else float(value)
        old_value: Any = getattr(self, key)

        if old_value is not None:
            if isinstance(final_value, tuple):
                if final_value == old_value: 
                    return False
            else:
                if not math.isclose(old_value, final_value, rel_tol=1e-4):
                    print(f"[WARNING] Conflict tại {key}: {old_value} vs {final_value}")
                if math.isclose(old_value, final_value, rel_tol=1e-6):
                    return False
        
        self.changed = True
        setattr(self, key, final_value)
        self.quan_li_do_thi.set(key, final_value, cong_thuc=method_name)  # type: ignore

        info: Dict[str, Any] = {
            "gia_tri": final_value if isinstance(final_value, tuple) else round(final_value, 2),
            "tu_cong_thuc": method_name
        }
        self.quan_li_do_thi.them_Doi_Tuong(key, loai, info)  # type: ignore
        self.new_values.add(key)

        explanation: str = f"Tìm được {key} = {final_value:.2f} qua {method_name}"
        if tu_cac_bien:
            explanation += f" từ các dữ liệu: {', '.join(tu_cac_bien)}"
        self.trace.append(explanation)

        if tu_cac_bien:
            for bien_goc in tu_cac_bien:
                self.quan_li_do_thi.them_canh(bien_goc, key, method_name)  # type: ignore

        if self.debug:
            if isinstance(final_value, tuple):
                print(f"[DEBUG] {key} = {final_value} ({method_name})")
            else:
                print(f"[DEBUG] {key} = {final_value:.4f} ({method_name})")
        return True
    
    def execute_alt(self):
        self.trace = []
        self.cache = set()
        self.is_valid = True
        self._sync_from_graph()

        is_ok, msg = self.validate()
        if not is_ok:
            self.error.append(msg)
            return
        
        self.tam_giac_can()
        self.tam_giac_vuong()
        self.tam_giac_vuong_can()
        self.tam_giac_deu()
        self.tam_giac_tu_nhon()
        self._sync_from_graph()

        hang_doi = deque([b for b in ["a","b","c","A","B","C","posA","posB","posC"] 
                         if getattr(self, b) is not None])
        da_xu_ly = set(hang_doi)

        while hang_doi and self.is_valid:
            bien = hang_doi.popleft()
            gia_tri_bien = getattr(self, bien) # Lấy giá trị thực để cache
            
            if bien in self.dependency_map:
                for ham in self.dependency_map[bien]:
                    # Truyền vào gia_tri_bien 
                    if self.check_cache(ham.__name__, gia_tri_bien): continue
                    
                    self.changed = False
                    ham() 

                    if self.changed:
                        self._sync_from_graph()
                        for b in ["a","b","c","A","B","C","S","P","R","r","h_a","h_b","h_c","l_a","l_b","l_c"]:
                            if getattr(self, b) is not None and b not in da_xu_ly:
                                hang_doi.append(b)
                                da_xu_ly.add(b)
    
    def check_cache(self, func_name: str, *args: Optional[float]) -> bool:
        # Tạo dấu vân tay cho lượt tính này
        signature = (func_name, tuple(round(x, 4) for x in args if x is not None))
        if signature in self.cache:
            return True # Đã tính với cùng 1 đầu vào, bỏ qua để tránh lặp vô hạn
        self.cache.add(signature)
        return False

    """Các luật và công thức"""
    def validate(self):
        for k in ["A", "B", "C"]:
            v = getattr(self, k)
            # Chỉ báo lỗi nếu người dùng nhập góc <= 0 hoặc >= 180
            # Nếu v là None (chưa có) thì bỏ qua không check
            if v is not None and v != 0: 
                if v <= 0 or v >= 180:
                    return False, f"Góc {k} không hợp lệ!"
        
        # Kiểm tra BĐT tam giác (giữ nguyên)
        if self.a and self.b and self.c:
            if not (self.a + self.b > self.c and self.a + self.c > self.b and self.b + self.c > self.a):
                return False, "Vi phạm bất đẳng thức tam giác!"
        
        return True, ""
    
    def tam_giac_can(self):
        """Chứng minh và kích hoạt dữ liệu tam giác cân"""

        if not self.dinh_can and self._has("a", "b", "c"):
            if self.b is not None and self.c is not None and math.isclose(self.b, self.c): self.dinh_can = "A"
            elif self.a is not None and self.c is not None and math.isclose(self.a, self.c): self.dinh_can = "B"
            elif self.a is not None and self.b is not None and math.isclose(self.a, self.b): self.dinh_can = "C"

        # Trường hợp 1: Nếu người dùng nhập vào là tam giác cân tại A
        if self.dinh_can == "A" or (self._has("B", "C") and self.B is not None and self.C is not None and math.isclose(self.B, self.C)):
            self.is_can = True
            changed = False
            
            if self._has("b") and not self._has("c"):
                self._save("c", "canh", self.b, "Tính chất tam giác cân tại A (b=c)")
                changed = True
            elif self._has("c") and not self._has("b"):
                self._save("b", "canh", self.c, "Tính chất tam giác cân tại A (c=b)")
                changed = True
            if self._has("B") and not self._has("C"):
                self._save("C", "goc", self.B, "Tính chất tam giác cân tại A (B=C)")
                changed = True
            return changed
        
        # Trường hợp 2: Nếu người dùng nhập vào là tam giác cân tại B
        if self.dinh_can == "B" or (self._has("A", "C") and self.A is not None and self.C is not None and math.isclose(self.A, self.C)):
            self.is_can = True
            changed = False
            
            if self._has("a") and not self._has("c"):
                self._save("c", "canh", self.a, "Tính chất tam giác cân tại B (a=c)")
                changed = True
            elif self._has("c") and not self._has("a"):
                self._save("a", "canh", self.c, "Tính chất tam giác cân tại B (c=a)")
                changed = True
            if self._has("A") and not self._has("C"):
                self._save("C", "goc", self.A, "Tính chất tam giác cân tại B (A=C)")
                changed = True
            return changed
        
        # Trường hợp 3: Nếu người dùng nhập vào là tam giác cân tại C
        if self.dinh_can == "C" or (self._has("A", "B") and self.A is not None and self.B is not None and math.isclose(self.A, self.B)):
            self.is_can = True
            changed = False
            
            if self._has("a") and not self._has("b"):
                self._save("b", "canh", self.a, "Tính chất tam giác cân tại C (a=b)")
                changed = True
            elif self._has("b") and not self._has("a"):
                self._save("a", "canh", self.b, "Tính chất tam giác cân tại C (b=a)")
                changed = True
            if self._has("A") and not self._has("B"):
                self._save("B", "goc", self.A, "Tính chất tam giác cân tại C (A=B)")
                changed = True
            return changed
        
        return False

    def tam_giac_deu(self):
        """Chứng minh và suy luận tam giác đều"""
        # Dấu hiệu: 3 cạnh bằng nhau OR 3 góc bằng nhau OR (Cân + 1 góc 60 độ)
        is_deu_sign = False
        if self._has("a","b","c") and self.a is not None and self.b is not None and self.c is not None and math.isclose(self.a, self.b) and math.isclose(self.b, self.c):
            is_deu_sign = True
        elif self._has("A","B","C") and self.A is not None and self.B is not None and math.isclose(self.A, 60) and math.isclose(self.B, 60):
            is_deu_sign = True
        elif self.is_can and self.A is not None and self.B is not None and self.C is not None and (math.isclose(self.A, 60) or math.isclose(self.B, 60) or math.isclose(self.C, 60)):
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
        if not self._has("a", "b", "c"):
            return False

        sides = sorted([(self.a, "A"), (self.b, "B"), (self.c, "C")], key=lambda x: x[0] if x[0] is not None else float('inf'))
        (a, _), (b, _), (c, C_name) = sides

        if a is None or b is None or c is None:
            return False

        if math.isclose(a**2 + b**2, c**2, rel_tol=1e-6):
            self.is_vuong = True
            self.dinh_vuong = C_name
            self._save(C_name, "goc", 90, "Tam giác vuông (Pytago)")
            return True

        elif a**2 + b**2 < c**2:
            self.is_tu = True
            self._save("is_tu", "tinh_chat", True, "Tam giác tù")
        else:
            self.is_tu = False
            self._save("is_tu", "tinh_chat", False, "Tam giác nhọn")
        return False
    
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
        
        # Nếu chưa có góc nhưng thỏa mãn a**2 + b**2 = c**2 (đảo)
        if not self.is_vuong and self._has("a", "b", "c"):
            sides = sorted([self.a, self.b, self.c], key=lambda x: x if x is not None else float('inf'))
            if self.a is not None and self.b is not None and self.c is not None and sides[0] is not None and sides[1] is not None and sides[2] is not None and math.isclose(sides[0]**2 + sides[1]**2, sides[2]**2, rel_tol=1e-6):
                self.is_vuong = True
                # Xác định đỉnh vuông là đối diện cạnh lớn nhất
                max_side = max(self.a, self.b, self.c)
                if max_side == self.a: self.dinh_vuong = "A"; self._save("A", "goc", 90, "Pytago đảo")
                elif max_side == self.b: self.dinh_vuong = "B"; self._save("B", "goc", 90, "Pytago đảo")
                else: self.dinh_vuong = "C"; self._save("C", "goc", 90, "Pytago đảo")

        # KÍCH HOẠT TÍNH TOÁN: Nếu đã biết là vuông tại đâu, tính cạnh thiếu ngay
        if self.is_vuong:
            if self.dinh_vuong == "A" and self.a is not None and self.b is not None: # Vuông tại A -> a là cạnh huyền
                val = self.a**2 - self.b**2
                if val <= 0: return False
                val = math.sqrt(val)
                if self.b and self.c and not self.a: return self._save("a", "canh", val, "Pytago")
                if self.a and self.b and not self.c: return self._save("c", "canh", val, "Pytago")
                if self.a and self.c and not self.b: return self._save("b", "canh", val, "Pytago")
            elif self.dinh_vuong == "B" and self.b is not None and self.a is not None: # Vuông tại B -> b là cạnh huyền
                val = self.b**2 - self.a**2
                if val <= 0: return False
                val = math.sqrt(val)
                if self.a and self.c and not self.b: return self._save("b", "canh", val, "Pytago")
                if self.b and self.c and not self.a: return self._save("a", "canh", val, "Pytago")
                if self.a and self.b and not self.c: return self._save("c", "canh", val, "Pytago")
            elif self.dinh_vuong == "C" and self.c is not None and self.a is not None: # Vuông tại C -> c là cạnh huyền
                val = self.c**2 - self.a**2
                if val <= 0: return False
                val = math.sqrt(val)
                if self.a and self.b and not self.c: return self._save("c", "canh", val, "Pytago")
                if self.a and self.c and not self.b: return self._save("b", "canh", val, "Pytago")
                if self.b and self.c and not self.a: return self._save("a", "canh", val, "Pytago")
        return False

    def tong3goc(self):
        if self._has("A", "B") and self.A is not None and self.B is not None and self.C is None:
            return self._save("C", "goc", 180 - self.A - self.B, "Tổng 3 góc", ["A", "B"])

        if self._has("A", "C") and self.A is not None and self.C is not None and self.B is None:
            return self._save("B", "goc", 180 - self.A - self.C, "Tổng 3 góc", ["A", "C"])

        if self._has("B", "C") and self.B is not None and self.C is not None and self.A is None:
            return self._save("A", "goc", 180 - self.B - self.C, "Tổng 3 góc", ["B", "C"])
        return False

    def chu_vi(self):
        """Chu vi tam giác"""
        if self._has("a", "b", "c") and self.a is not None and self.b is not None and self.c is not None and self.quan_li_do_thi.get("P") is None: # type: ignore
            return self._save("P","chu_vi", self.a + self.b + self.c, "Chu vi từ a, b, c", ["a", "b", "c"])
        if self._has("S","r") and self.S is not None and self.r is not None and not self._has("P"):
            return self._save("P", "chu_vi", (2 * self.S) / self.r, "Chu vi từ S và r", ["S", "r"])
        if self._has("R","A", "B", "C") and self.R is not None and self.A is not None and self.B is not None and self.C is not None and not self._has("P"):
            return self._save("P", "chu_vi", 2 * self.R * (math.sin(math.radians(self.A)) + 
                               math.sin(math.radians(self.B)) + 
                               math.sin(math.radians(self.C))), "Chu vi từ R và 3 góc", ["R", "A", "B", "C"])
        if self.debug and True:
            print("Đã áp dụng công thức Chu Vi")

    def heron(self):
        """Diện tích tam giác theo công thức Heron"""
        if self._has("a", "b", "c") and self.a is not None and self.b is not None and self.c is not None and self.quan_li_do_thi.get("S") is None:  # type: ignore
            p = (self.a + self.b + self.c) / 2
            S_value = math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))
            return self._save("S","dien_tich", S_value, "Diện tích từ công thức Heron", ["a", "b", "c"])
        if self.debug and True:
            print("Đã áp dụng công thức Heron")

    def pytago(self):   
        """Chỉ áp dụng nếu là tam giác vuông (giả sử góc C=90) hoặc biết 2 cạnh"""

        if not self.is_vuong or not self.dinh_vuong: 
            return False
        
        if self.dinh_vuong == "A":
            if self._has("b", "c") and self.b is not None and self.c is not None and not self._has("a"):
                S_value= self.b**2 + self.c**2
                if S_value <= 0: return False
                S_value = math.sqrt(S_value)
                return self._save("a", "canh", S_value, "Pytago", ["b", "c"])
            if self._has("a", "c") and self.a is not None and self.c is not None and not self._has("b"):
                S_value = math.sqrt(self.a**2 - self.c**2)
                if S_value <= 0: return False
                return self._save("b", "canh", S_value, "Pytago", ["a", "c"])
            if self._has("a", "b") and self.a is not None and self.b is not None and not self._has("c"):
                S_value = math.sqrt(self.a**2 - self.b**2)
                if S_value <= 0: return False
                return self._save("c", "canh", S_value, "Pytago", ["a", "b"])
            
        elif self.dinh_vuong == "B":
            if self._has("a", "c") and self.a is not None and self.c is not None and not self._has("b"):
                S_value = math.sqrt(self.a**2 + self.c**2)
                if S_value <= 0: return False
                return self._save("b", "canh", S_value, "Pytago", ["a", "c"])
            if self._has("b", "c") and self.b is not None and self.c is not None and not self._has("a"):
                S_value = math.sqrt(self.b**2 - self.c**2)
                if S_value <= 0: return False
                return self._save("a", "canh", S_value, "Pytago", ["b", "c"])
            if self._has("a", "b") and self.a is not None and self.b is not None and not self._has("c"):
                S_value = math.sqrt(self.b**2 - self.a**2)
                if S_value <= 0: return False
                return self._save("c", "canh", S_value, "Pytago", ["a", "b"])
            
        elif self.dinh_vuong == "C":
            if self._has("a", "b") and self.a is not None and self.b is not None and not self._has("c"):
                S_value = math.sqrt(self.a**2 + self.b**2)
                if S_value <= 0: return False
                return self._save("c", "canh", S_value, "Pytago", ["a", "b"])
            if self._has("a", "c") and self.a is not None and self.c is not None and not self._has("b"):
                S_value = math.sqrt(self.c**2 - self.a**2)
                if S_value <= 0: return False
                return self._save("b", "canh", S_value, "Pytago", ["a", "c"])
            if self._has("b", "c") and self.b is not None and self.c is not None and not self._has("a"):
                S_value = math.sqrt(self.c**2 - self.b**2)
                if S_value <= 0: return False
                return self._save("a", "canh", S_value, "Pytago", ["b", "c"])
            
        if self.debug and True:
            print("Đã áp dụng định lý Pytago")

    def dinh_ly_sin(self):
        if self._has("a","A") and self.a is not None and self.A is not None and not self._has("R"):
            den = math.sin(math.radians(self.A))
            if abs(den) < 1e-9:
                return False
            return self._save("R", "ban_kinh", self.a / (2 * den), "Định lý Sin", ["a", "A"])
        if self._has("b", "B") and self.b is not None and self.B is not None and not self._has("R"):
            den = math.sin(math.radians(self.B))
            if abs(den) < 1e-9:
                return False
            return self._save("R", "ban_kinh", self.b / (2 * den), "Định lý Sin", ["b", "B"])
        if self._has("c", "C") and self.c is not None and self.C is not None and not self._has("R"):
            den = math.sin(math.radians(self.C))
            if abs(den) < 1e-9:
                return False
            return self._save("R", "ban_kinh", self.c / (2 * den), "Định lý Sin", ["c", "C"])

        if self._has("R","A") and self.R is not None and self.A is not None and not self._has("a"):
            den = math.sin(math.radians(self.A))
            if abs(den) < 1e-9:
                return False
            return self._save("a", "canh", 2 * self.R * den, "Định lý Sin", ["R", "A"])
        if self._has("R","B") and self.R is not None and self.B is not None and not self._has("b"):
            den = math.sin(math.radians(self.B))
            if abs(den) < 1e-9:
                return False
            return self._save("b", "canh", 2 * self.R * den, "Định lý Sin", ["R", "B"])
        if self._has("R", "C") and self.R is not None and self.C is not None and not self._has("c"):
            den = math.sin(math.radians(self.C))
            if abs(den) < 1e-9:
                return False
            return self._save("c", "canh", 2 * self.R * den, "Định lý Sin", ["R", "C"])
        
        if self._has("a","A","B") and self.a is not None and self.A is not None and self.B is not None and not self._has("b"):
            den_A = math.sin(math.radians(self.A))
            den_B = math.sin(math.radians(self.B))
            if abs(den_A) < 1e-9 or abs(den_B) < 1e-9:
                return False
            val = (self.a * den_B) / den_A
            return self._save("b", "canh", val, "Định lý Sin", ["a", "A", "B"])
        if self._has("a", "A", "C") and self.a is not None and self.A is not None and self.C is not None and not self._has("c"):
            den_A = math.sin(math.radians(self.A))
            den_C = math.sin(math.radians(self.C))
            if abs(den_A) < 1e-9 or abs(den_C) < 1e-9:
                return False
            val = (self.a * den_C) / den_A
            return self._save("c", "canh", val, "Định lý Sin", ["a", "A", "C"])
        if self._has("b", "B", "A") and self.b is not None and self.B is not None and self.A is not None and not self._has("a"):
            den_A = math.sin(math.radians(self.A))
            den_B = math.sin(math.radians(self.B))
            if abs(den_A) < 1e-9 or abs(den_B) < 1e-9:
                return False
            val = (self.b * den_A) / den_B
            return self._save("a", "canh", val, "Định lý Sin", ["b", "B", "A"])
        if self._has("b", "B", "C") and self.b is not None and self.B is not None and self.C is not None and not self._has("c"):
            den_B = math.sin(math.radians(self.B))
            den_C = math.sin(math.radians(self.C))
            if abs(den_B) < 1e-9 or abs(den_C) < 1e-9:
                return False
            val = (self.b * den_C) / den_B
            return self._save("c", "canh", val, "Định lý Sin", ["b", "B", "C"])
        if self._has("c", "C", "A") and self.c is not None and self.C is not None and self.A is not None and not self._has("a"):
            den_A = math.sin(math.radians(self.A))
            den_C = math.sin(math.radians(self.C))
            if abs(den_A) < 1e-9 or abs(den_C) < 1e-9:
                return False
            val = (self.c * den_A) / den_C
            return self._save("a", "canh", val, "Định lý Sin", ["c", "C", "A"])
        if self._has("c", "C", "B") and self.c is not None and self.C is not None and self.B is not None and not self._has("b"):
            den_B = math.sin(math.radians(self.B))
            den_C = math.sin(math.radians(self.C))
            if abs(den_B) < 1e-9 or abs(den_C) < 1e-9:
                return False
            val = (self.c * den_B) / den_C
            return self._save("b", "canh", val, "Định lý Sin", ["c", "C", "B"])
        
        if self._has("a", "A", "b") and self.a is not None and self.A is not None and self.b is not None and not self._has("B") and self.B is not None:
            den_A = math.sin(math.radians(self.A))
            den_B = math.sin(math.radians(self.B))
            if abs(den_A) < 1e-9 or abs(den_B) < 1e-9:
                return False
            sin_B = (self.b * den_A) / self.a
            # Kiểm tra điều kiện sin <= 1 để tránh lỗi math domain
            if -1 <= sin_B <= 1:
                val_B = math.degrees(math.asin(sin_B))
                return self._save("B", "goc", val_B, "Định lý Sin", ["a", "A", "b"])
            
        if self._has("a", "A", "c") and self.a is not None and self.A is not None and self.c is not None and not self._has("C") and self.C is not None:
            den_A = math.sin(math.radians(self.A))
            den_C = math.sin(math.radians(self.C))
            if abs(den_A) < 1e-9 or abs(den_C) < 1e-9:
                return False
            sin_C = (self.c * den_A) / self.a
            if -1 <= sin_C <= 1:
                val_C = math.degrees(math.asin(sin_C))
                return self._save("C", "goc", val_C, "Định lý Sin", ["a", "A", "c"])
        
        if self._has("b", "B", "a") and self.b is not None and self.B is not None and self.a is not None and not self._has("A") and self.A is not None:
            den_A = math.sin(math.radians(self.A))
            den_B = math.sin(math.radians(self.B))
            if abs(den_A) < 1e-9 or abs(den_B) < 1e-9:
                return False
            sin_A = (self.a * den_B) / self.b
            if -1 <= sin_A <= 1:
                val_A = math.degrees(math.asin(sin_A))
                return self._save("A", "goc", val_A, "Định lý Sin", ["b", "B", "a"])
        
        if self._has("b", "B", "c") and self.b is not None and self.B is not None and self.c is not None and not self._has("C") and self.C is not None:
            den_B = math.sin(math.radians(self.B))
            den_C = math.sin(math.radians(self.C))
            if abs(den_B) < 1e-9 or abs(den_C) < 1e-9:
                return False
            sin_C = (self.c * den_B) / self.b
            if -1 <= sin_C <= 1:
                val_C = math.degrees(math.asin(sin_C))
                return self._save("C", "goc", val_C, "Định lý Sin", ["b", "B", "c"])
        
        if self._has("c", "C", "a") and self.c is not None and self.C is not None and self.a is not None and not self._has("A") and self.A is not None:
            den_A = math.sin(math.radians(self.A))
            den_C = math.sin(math.radians(self.C))
            if abs(den_A) < 1e-9 or abs(den_C) < 1e-9:
                return False
            sin_A = (self.a * den_C) / self.c
            if -1 <= sin_A <= 1:
                val_A = math.degrees(math.asin(sin_A))
                return self._save("A", "goc", val_A, "Định lý Sin", ["c", "C", "a"])
        
        if self._has("c", "C", "b") and self.c is not None and self.C is not None and self.b is not None and not self._has("B") and self.B is not None:
            den_B = math.sin(math.radians(self.B))
            den_C = math.sin(math.radians(self.C))
            if abs(den_B) < 1e-9 or abs(den_C) < 1e-9:
                return False
            sin_B = (self.b * den_C) / self.c
            if -1 <= sin_B <= 1:
                val_B = math.degrees(math.asin(sin_B))
                return self._save("B", "goc", val_B, "Định lý Sin", ["c", "C", "b"])
        
        if self._has("R", "C") and self.R is not None and self.C is not None and not self._has("c"):
            val_c = 2 * self.R * math.sin(math.radians(self.C))
            return self._save("c", "canh", val_c, "Định lý Sin", ["R", "C"])
        if self._has("R", "B") and self.R is not None and self.B is not None and not self._has("b"):
            den_B = math.sin(math.radians(self.B))
            if abs(den_B) < 1e-9:
                return False
            val_b = 2 * self.R * den_B
            return self._save("b", "canh", val_b, "Định lý Sin", ["R", "B"])
        if self._has("R", "A") and self.R is not None and self.A is not None and not self._has("a"):
            den_A = math.sin(math.radians(self.A))
            if abs(den_A) < 1e-9:
                return False
            val_a = 2 * self.R * den_A
            return self._save("a", "canh", val_a, "Định lý Sin", ["R", "A"])
        
        if self.debug and True:
            print("Đã áp dụng định lý Sin")

    def dinh_ly_cos(self):
        if self._has("a", "b", "c") and self.a is not None and self.b is not None and self.c is not None and not self._has("A"):
            # Tính góc A từ công thức định lý cosin
            cos_A = (self.b**2 + self.c**2 - self.a**2) / (2 * self.b * self.c)
            cos_A = max(-1, min(1, cos_A))  # Đảm bảo cos_A nằm trong khoảng [-1, 1] để tránh lỗi math domain
            A_value = math.degrees(math.acos(cos_A))
            return self._save("A", "goc", A_value, "Định lý Cosin", ["a", "b", "c"])
        if self._has("a", "b", "c") and self.a is not None and self.b is not None and self.c is not None and not self._has("B"):
            # Tính góc B từ công thức định lý cosin
            cos_B = (self.a**2 + self.c**2 - self.b**2) / (2 * self.a * self.c)
            cos_B = max(-1, min(1, cos_B))  # Đảm bảo cos_B nằm trong khoảng [-1, 1] để tránh lỗi math domain
            B_value = math.degrees(math.acos(cos_B))
            return self._save("B", "goc", B_value, "Định lý Cosin", ["a", "b", "c"])
        if self._has("a", "b", "c") and self.a is not None and self.b is not None and self.c is not None and not self._has("C"):
            # Tính góc C từ công thức định lý cosin
            cos_C = (self.a**2 + self.b**2 - self.c**2) / (2 * self.a * self.b)
            cos_C = max(-1, min(1, cos_C))  # Đảm bảo cos_C nằm trong khoảng [-1, 1] để tránh lỗi math domain
            C_value = math.degrees(math.acos(cos_C))
            return self._save("C", "goc", C_value, "Định lý Cosin", ["a", "b", "c"])
        
        if self._has("a", "b", "C") and self.a is not None and self.b is not None and self.C is not None and not self._has("c"):
            c_val = math.sqrt(self.a**2 + self.b**2 - 2*self.a*self.b*math.cos(math.radians(self.C)))
            return self._save("c", "canh", c_val, "Định lý Cosin", ["a", "b", "C"])
        if self._has("a", "c", "B") and self.a is not None and self.c is not None and self.B is not None and not self._has("b"):
            b_val = math.sqrt(self.a**2 + self.c**2 - 2*self.a*self.c*math.cos(math.radians(self.B)))
            return self._save("b", "canh", b_val, "Định lý Cosin", ["a", "c", "B"])
        if self._has("b", "c", "A") and self.b is not None and self.c is not None and self.A is not None and not self._has("a"):
            a_val = math.sqrt(self.b**2 + self.c**2 - 2*self.b*self.c*math.cos(math.radians(self.A)))
            return self._save("a", "canh", a_val, "Định lý Cosin", ["b", "c", "A"])
        
        if self.debug and True:
            print("Đã áp dụng định lý Cosin")

    def duong_trung_tuyen(self):
        """Đường trung tuyến: m_a = 0.5 * sqrt(2*b**2 + 2*c**2 - a**2)"""
        if self._has("a", "b", "c") and self.a is not None and self.b is not None and self.c is not None and self.quan_li_do_thi.get("m_a") is None:  # type: ignore
            m_a_value = 0.5 * math.sqrt(2 * self.b**2 + 2 * self.c**2 - self.a**2)
            return self._save("m_a", "duong_trung_tuyen", m_a_value, "Công thức Đường Trung Tuyến", ["a", "b", "c"])
        if self._has("a", "b", "c") and self.a is not None and self.b is not None and self.c is not None and self.quan_li_do_thi.get("m_b") is None:  # type: ignore
            m_b_value = 0.5 * math.sqrt(2 * self.a**2 + 2 * self.c**2 - self.b**2)
            return self._save("m_b", "duong_trung_tuyen", m_b_value, "Công thức Đường Trung Tuyến", ["a", "b", "c"])
        if self._has("a", "b", "c") and self.a is not None and self.b is not None and self.c is not None and self.quan_li_do_thi.get("m_c") is None:  # type: ignore
            m_c_value = 0.5 * math.sqrt(2 * self.a**2 + 2 * self.b**2 - self.c**2)
            return self._save("m_c", "duong_trung_tuyen", m_c_value, "Công thức Đường Trung Tuyến", ["a", "b", "c"])
        
        if self.debug and True:
            print("Đã áp dụng công thức Đường Trung Tuyến")

    # Diện tích qua bán kính đường tròn ngoại tiếp R: S = (abc) / (4R)
    def dien_tich_ngoai_tiep(self):

        if self._has("a", "b", "c", "S") and self.a is not None and self.b is not None and self.c is not None and self.S is not None and self.quan_li_do_thi.get("R") is None:  # type: ignore
            R_val = (self.a * self.b * self.c) / (4 * self.S)
            return self._save("R", "ban_kinh", R_val, "Công thức diện tích ngoại tiếp", ["a", "b", "c", "S"])
        if self._has("a", "b", "c", "R") and self.a is not None and self.b is not None and self.c is not None and self.R is not None and self.quan_li_do_thi.get("S") is None:  # type: ignore
            S_val = (self.a * self.b * self.c) / (4 * self.R)
            return self._save("S", "dien_tich", S_val, "Công thức diện tích ngoại tiếp", ["a", "b", "c", "R"])
        if self.debug and True:
            print("Đã áp dụng công thức diện tích ngoại tiếp")

    # Diện tích qua bán kính nội tiếp r: S = p * r
    def dien_tich_noi_tiep(self):
        
        if self._has("a", "b", "c") and self.a is not None and self.b is not None and self.c is not None:
            p = (self.a + self.b + self.c) / 2
            if not self._has("S") and self._has("r") and self.r is not None:
                S_val = p * self.r
                return self._save("S", "dien_tich", S_val, "S = p*r", ["a", "b", "c", "r"])
            if self._has("S") and not self._has("r") and self.S is not None:
                r_val = self.S / p
                return self._save("r", "ban_kinh_noi_tiep", r_val, "r = S/p", ["a", "b", "c", "S"])
            
        if self.debug and True:
            print("Đã áp dụng công thức diện tích nội tiếp")

    # Diện tích qua 2 cạnh và góc xen giữa: S = 0.5 * a * b * sin(C)
    def dien_tich_sin_goc(self):

        if self._has("a", "b", "C") and self.a is not None and self.b is not None and self.C is not None and not self._has("S"):
            S_val = 0.5 * self.a * self.b * math.sin(math.radians(self.C))
            return self._save("S", "dien_tich", S_val, "S = 1/2*ab*sinC", ["a", "b", "C"])
        # 2. Trường hợp biết cạnh b, c và góc A (Tăng tính liên kết)
        if self._has("b", "c", "A") and self.b is not None and self.c is not None and self.A is not None and not self._has("S"):
            S_val = 0.5 * self.b * self.c * math.sin(math.radians(self.A))
            return self._save("S", "dien_tich", S_val, "S = 1/2 * b * c * sin(A)", ["b", "c", "A"])
        # 3. Trường hợp biết cạnh a, c và góc B
        if self._has("a", "c", "B") and self.a is not None and self.c is not None and self.B is not None and not self._has("S"):
            S_val = 0.5 * self.a * self.c * math.sin(math.radians(self.B))
            return self._save("S", "dien_tich", S_val, "S = 1/2 * a * c * sin(B)", ["a", "c", "B"])
        if self.debug and True:
            print("Đã áp dụng công thức diện tích sin góc")

    def duong_cao(self):
        """Đường cao: h = 2S / cạnh_tương_ứng"""
        # 1. Tính h_a
        if self._has("S") and self.S is not None and self._has("a") and self.a is not None and not self._has("h_a"):
            val = (2 * self.S) / self.a
            return self._save("h_a", "duong_cao", val, "h_a = 2S / a", ["S", "a"])

        # 2. Tính h_b
        if self._has("S") and self.S is not None and self._has("b") and self.b is not None and not self._has("h_b"):
            val = (2 * self.S) / self.b
            return self._save("h_b", "duong_cao", val, "h_b = 2S / b", ["S", "b"])

        # 3. Tính h_c
        if self._has("S") and self.S is not None and self._has("c") and self.c is not None and not self._has("h_c"):
            val = (2 * self.S) / self.c
            return self._save("h_c", "duong_cao", val, "h_c = 2S / c", ["S", "c"])
        if self.debug and True:
            print("Đã áp dụng công thức đường cao")

    # Đường phân giác trong: l_a = (2bc * cos(A/2)) / (b+c)
    def duong_phan_giac(self):

        if self._has("b", "c", "A") and self.b is not None and self.c is not None and self.A is not None and not self._has("l_a"):
            la_val = (2 * self.b * self.c * math.cos(math.radians(self.A / 2))) / (self.b + self.c)
            return self._save("l_a", "phan_giac", la_val, "Công thức phân giác", ["b", "c", "A"])
        if self._has("a", "c", "B") and self.a is not None and self.c is not None and self.B is not None and not self._has("l_b"):
            lb_val = (2 * self.a * self.c * math.cos(math.radians(self.B / 2))) / (self.a + self.c)
            return self._save("l_b", "phan_giac", lb_val, "Công thức phân giác", ["a", "c", "B"])
        if self._has("a", "b", "C") and self.a is not None and self.b is not None and self.C is not None and not self._has("l_c"):
            lc_val = (2 * self.a * self.b * math.cos(math.radians(self.C / 2))) / (self.a + self.b)
            return self._save("l_c", "phan_giac", lc_val, "Công thức phân giác", ["a", "b", "C"])
        if self.debug and True:
            print("Đã áp dụng công thức đường phân giác")

    # Tính chất đường phân giác (tỉ lệ đoạn thẳng trên cạnh đáy d_b, d_c)
    def ti_le_phan_giac(self):
        if self._has("b", "c", "a") and self.b is not None and self.c is not None and self.a is not None and not self._has("d_b"):
            db_val = (self.c * self.a) / (self.b + self.c)
            dc_val = self.a - db_val
            # Dùng _save thay vì v.set
            res1 = self._save("d_b", "doan", db_val, "Phân giác", ["a","b","c"])
            res2 = self._save("d_c", "doan", dc_val, "Phân giác", ["a","b","c"])
            return res1 or res2
        return False

    def tam_ngoai_tiep(self):

        if self._has("posA", "posB", "posC") and self.posA is not None and self.posB is not None and self.posC is not None and not self._has("posO"):
            pA, pB, pC = self.posA, self.posB, self.posC
            x1, y1 = pA
            x2, y2 = pB
            x3, y3 = pC
            D = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
            if D == 0: return False 
            ux = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / D
            uy = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / D
            # Chuyển sang _save
            return self._save("posO", "tam", (ux, uy), "Tọa độ tâm ngoại tiếp", ["posA", "posB", "posC"])
        return False
    
    def tam_noi_tiep(self):

        if self._has("posA", "posB", "posC", "a", "b", "c") and self.posA is not None and self.posB is not None and self.posC is not None and self.a is not None and self.b is not None and self.c is not None and not self._has("posI"):
            pA, pB, pC = self.posA, self.posB, self.posC
            chu_vi = self.a + self.b + self.c
            ix = (self.a * pA[0] + self.b * pB[0] + self.c * pC[0]) / chu_vi
            iy = (self.a * pA[1] + self.b * pB[1] + self.c * pC[1]) / chu_vi
            # Chuyển sang _save
            return self._save("posI", "tam", (ix, iy), "Tọa độ tâm nội tiếp", ["posA", "posB", "posC", "a", "b", "c"])
        return False