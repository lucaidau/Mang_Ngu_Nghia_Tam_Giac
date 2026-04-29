# File: controller.py
from app.models.quanLiDoThi import QuanLiDoThi
from app.models.congThuc  import Rules
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

    def thuc_thi_suy_dien(self):
        """Kích hoạt bộ quy tắc suy diễn"""
        print("--- Đang thực hiện suy diễn ---")
        self.rules.execute_alt()
        
        if self.rules.error:
            self._status_message = "\n".join(self.rules.error)
            print(f"Lỗi suy diễn: {self._status_message}")

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
            if val is None or isinstance(val, (list, tuple)): continue  # skip coordinates
            
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

        import tkinter as tk
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import matplotlib.patches as mpatches

        # Tạo cửa sổ Toplevel thay vì plt.show() để tránh conflict với tkinter mainloop
        top = tk.Toplevel()
        top.title("Mạng Ngữ Nghĩa Tam Giác")
        top.geometry("1100x750")
        top.configure(bg="#0d1117")

        fig = Figure(figsize=(13, 8), facecolor="#0d1117")
        ax  = fig.add_subplot(111)
        ax.set_facecolor("#0d1117")

        pos = nx.spring_layout(G, k=5.0, iterations=100, seed=50)

        # Node labels
        labels = {}
        for node, attr in G.nodes(data=True):
            val = attr.get("gia_tri")
            if val is not None and not isinstance(val, (list, tuple)):
                labels[node] = f"{node}\n({round(float(val), 3)})"
            else:
                labels[node] = node

        # Color map
        side_keys   = {"a", "b", "c"}
        angle_keys  = {"A", "B", "C"}
        radius_keys = {"R", "r"}
        area_keys   = {"S", "P"}

        color_map = []
        for node in G.nodes():
            if node in side_keys:        color_map.append("#58a6ff")
            elif node in angle_keys:     color_map.append("#3fb950")
            elif node in radius_keys:    color_map.append("#f78166")
            elif node in area_keys:      color_map.append("#d2a8ff")
            else:                        color_map.append("#ffd700")

        nx.draw_networkx_nodes(G, pos, node_color=color_map,
                               node_size=3200, ax=ax, alpha=0.95)
        nx.draw_networkx_labels(G, pos, labels=labels,
                                font_size=8, font_weight="bold",
                                font_color="#0d1117", ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color="#58a6ff",
                               width=1.5, ax=ax, alpha=0.35)
        edge_labels = nx.get_edge_attributes(G, "relation")
        nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels=edge_labels,
            font_size=7,
            font_color="#ffd700",
            bbox=dict(
                boxstyle="round,pad=0.25",
                facecolor="#1c2128",
                edgecolor="#30363d",
                alpha=0.85,
            ),
            ax=ax,
        )

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
        fig.tight_layout()

        # Nhúng figure vào cửa sổ tkinter — không dùng plt.show()
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Nút đóng
        tk.Button(top, text="✕  Đóng", font=("Courier New", 10, "bold"),
                  bg="#f78166", fg="#0d1117", relief="flat", padx=16, pady=6,
                  cursor="hand2", command=top.destroy).pack(pady=(0, 10))