# File: controller.py
from app.models.quanLiDoThi import QuanLiDoThi
from app.models.congThuc  import Rules
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import math

class Controller:
    def __init__(self, view=None):
        self.view = view
        self.qldt = QuanLiDoThi()
        self.rules = Rules(self.qldt)
        self._status_message = ""

    def set_view(self, view):
        self.view = view

    def nhap_du_lieu_ban_dau(self, data_dict: dict):
        """Nhận dữ liệu từ view và nạp vào đồ thị"""
        print("--- Đang nạp dữ liệu đầu vào ---")
        for key, value in data_dict.items():
            if not value: continue
            try:
                gia_tri = float(value)
                self.qldt.set(key, gia_tri, "Dữ liệu nhập")
            except (ValueError, TypeError):
                print(f"Cảnh báo: Giá trị '{value}' của {key} không hợp lệ.")

    def validate_tam_giac(self, a, b, c, deg_A, deg_B, deg_C):
        if any(val <= 0 for val in [a, b, c, deg_A, deg_B, deg_C]):
            return False, "Các cạnh và góc phải lớn hơn 0"
        if not math.isclose(deg_A + deg_B + deg_C, 180, rel_tol=1e-5):
            return False, "Tổng 3 góc phải là 180 độ"
        if not (a + b > c and a + c > b and b + c > a):
            return False, "Vi phạm bất đẳng thức tam giác"
        return True, "Hợp lệ"

    def thuc_thi_suy_dien(self):
        """Kích hoạt bộ quy tắc suy diễn"""
        print("--- Đang thực hiện suy diễn ---")
        self.rules.execute_alt()

    def lay_ket_qua_dinh_dang(self) -> str:
        """Lấy danh sách các giá trị tìm được, nhóm theo loại"""
        graph = self.qldt.lay_do_thi()
        
        groups = {
            "CẠNH": [],
            "GÓC (độ)": [],
            "DIỆN TÍCH & CHU VI": [],
            "BÁN KÍNH": [],
            "ĐƯỜNG ĐẶC BIỆT": [],
        }
        
        side_keys  = {"a", "b", "c"}
        angle_keys = {"A", "B", "C"}
        area_keys  = {"S", "P"}
        radius_keys = {"R", "r"}
        special_keys = {"ha", "hb", "hc", "la", "lb", "lc", "m_a", "m_b", "m_c"}
        
        for node, attr in graph.nodes(data=True):
            val = attr.get("gia_tri")
            if val is None: continue
            if isinstance(val, (list, tuple)): continue  # skip coordinates
            
            line = f"{node} = {float(val):.4f}"
            if node in side_keys:
                groups["CẠNH"].append(line)
            elif node in angle_keys:
                groups["GÓC (độ)"].append(line)
            elif node in area_keys:
                groups["DIỆN TÍCH & CHU VI"].append(line)
            elif node in radius_keys:
                groups["BÁN KÍNH"].append(line)
            elif node in special_keys:
                groups["ĐƯỜNG ĐẶC BIỆT"].append(line)
        
        result_lines = []
        for group_name, lines in groups.items():
            if lines:
                result_lines.append(f"[{group_name}]")
                result_lines.extend(sorted(lines))
                result_lines.append("")
        
        return "\n".join(result_lines) if result_lines else "Không có kết quả."

    def lay_vet_suy_dien_dinh_dang(self) -> str:
        """Lấy trình tự các bước giải"""
        traces = []
        graph = self.qldt.lay_do_thi()
        for node, attr in graph.nodes(data=True):
            formula = attr.get("cong_thuc")
            if formula and formula != "Input" and formula != "Dữ liệu nhập":
                val = attr.get("gia_tri")
                if val is not None and not isinstance(val, (list, tuple)):
                    traces.append(f"Tìm {node} = {float(val):.4f}  ←  {formula}")
        return "\n".join(traces) if traces else "Không có vết suy diễn."

    def lay_tom_tat(self) -> str:
        """Tóm tắt ngắn gọn kết quả và loại tam giác"""
        lines = []
        r = self.rules
        loai = self.lay_loai_tam_giac()
        lines.append(f"Loại tam giác: {loai}\n")
        
        if r.a and r.b and r.c:
            lines.append(f"Ba cạnh:  a={r.a:.4f}, b={r.b:.4f}, c={r.c:.4f}")
        if r.A and r.B and r.C:
            lines.append(f"Ba góc:   A={r.A:.2f}°, B={r.B:.2f}°, C={r.C:.2f}°")
        if r.S:
            lines.append(f"Diện tích: S = {r.S:.4f}")
        if r.P:
            lines.append(f"Chu vi:    P = {r.P:.4f}")
        if r.R:
            lines.append(f"Bán kính ngoại tiếp: R = {r.R:.4f}")
        if r.r:
            lines.append(f"Bán kính nội tiếp:   r = {r.r:.4f}")
        return "\n".join(lines)

    def lay_loai_tam_giac(self) -> str:
        """Xác định loại tam giác"""
        r = self.rules
        loai_parts = []
        if r.is_deu:
            loai_parts.append("Đều")
        else:
            if r.is_can:
                loai_parts.append("Cân")
            if r.is_vuong:
                loai_parts.append("Vuông")
            elif r.is_tu:
                loai_parts.append("Tù")
            else:
                loai_parts.append("Nhọn")
        return "Tam giác " + " + ".join(loai_parts) if loai_parts else "Tam giác thường"

    def lay_du_lieu_tam_giac(self) -> dict:
        """Trả về dict dữ liệu để vẽ tam giác trên canvas"""
        r = self.rules
        return {
            "a": r.a, "b": r.b, "c": r.c,
            "A": r.A, "B": r.B, "C_angle": r.C,
            "S": r.S, "R": r.R, "r": r.r,
        }

    def reset(self):
        """Làm mới toàn bộ dữ liệu"""
        self.qldt = QuanLiDoThi()
        self.rules = Rules(self.qldt)

    def ve_do_thi(self):
        G = self.qldt.lay_do_thi()
        if not G.nodes():
            return

        fig, ax = plt.subplots(figsize=(14, 9))
        fig.patch.set_facecolor("#0d1117")
        ax.set_facecolor("#0d1117")

        pos = nx.spring_layout(G, k=5.0, iterations=100, seed=50)

        # Node labels with values
        labels = {}
        for node, attr in G.nodes(data=True):
            val = attr.get("gia_tri")
            if val is not None and not isinstance(val, (list, tuple)):
                labels[node] = f"{node}\n({round(float(val), 3)})"
            else:
                labels[node] = node

        # Color map by type
        side_keys   = {"a", "b", "c"}
        angle_keys  = {"A", "B", "C"}
        radius_keys = {"R", "r"}
        area_keys   = {"S", "P"}
        
        color_map = []
        for node, attr in G.nodes(data=True):
            if node in side_keys:
                color_map.append("#58a6ff")   # blue – sides
            elif node in angle_keys:
                color_map.append("#3fb950")   # green – angles
            elif node in radius_keys:
                color_map.append("#f78166")   # red – radii
            elif node in area_keys:
                color_map.append("#d2a8ff")   # purple – area/perimeter
            else:
                color_map.append("#ffd700")   # gold – special lines

        nx.draw_networkx_nodes(G, pos, node_color=color_map,
                               node_size=3200, ax=ax, alpha=0.95)
        nx.draw_networkx_labels(G, pos, labels=labels,
                                font_size=8, font_weight="bold",
                                font_color="#0d1117", ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color="#30363d",
                               width=2, ax=ax, alpha=0.8)

        edge_labels = nx.get_edge_attributes(G, "relation")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                     font_size=7, font_color="#8b949e", ax=ax)

        # Legend
        legend_items = [
            mpatches.Patch(color="#58a6ff", label="Cạnh (a, b, c)"),
            mpatches.Patch(color="#3fb950", label="Góc (A, B, C)"),
            mpatches.Patch(color="#d2a8ff", label="Diện tích / Chu vi"),
            mpatches.Patch(color="#f78166", label="Bán kính (R, r)"),
            mpatches.Patch(color="#ffd700", label="Đường đặc biệt"),
        ]
        ax.legend(handles=legend_items, loc="upper left",
                  facecolor="#161b22", edgecolor="#30363d",
                  labelcolor="white", fontsize=9)

        ax.set_title("MẠNG NGỮ NGHĨA TAM GIÁC",
                     color="#58a6ff", fontsize=14, fontweight="bold",
                     fontfamily="monospace", pad=16)
        ax.axis("off")
        plt.tight_layout()
        plt.show()
