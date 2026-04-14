# File: controller.py
from app.models.quanLiDoThi import QuanLiDoThi
from app.models.congThuc  import Rules
import matplotlib.pyplot as plt
import networkx as nx

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
                # Nạp vào QuanLiDoThi
                self.qldt.set(key, gia_tri, "Dữ liệu nhập")
            except (ValueError, TypeError):
                print(f"Cảnh báo: Giá trị '{value}' của {key} không hợp lệ.")

    def thuc_thi_suy_dien(self):
        """Kích hoạt bộ quy tắc suy diễn"""
        print("--- Đang thực hiện suy diễn ---")
        self.rules.execute_alt()

    def lay_ket_qua_dinh_dang(self) -> str:
        """Lấy danh sách các giá trị tìm được"""
        graph = self.qldt.lay_do_thi()
        results = []
        for node, attr in graph.nodes(data=True):
            val = attr.get("gia_tri")
            if val is not None:
                results.append(f"{node} = {val:.2f}")
        return "\n".join(results) if results else "Không có kết quả."

    def lay_vet_suy_dien_dinh_dang(self) -> str:
        """Lấy trình tự các bước giải"""
        traces = []
        graph = self.qldt.lay_do_thi()
        for node, attr in graph.nodes(data=True):
            formula = attr.get("cong_thuc")
            if formula and formula != "Input":
                traces.append(f"Tìm được {node} qua: {formula}")
        return "\n".join(traces) if traces else "Không có vết suy diễn."

    def reset(self):
        """Làm mới toàn bộ dữ liệu"""
        self.qldt = QuanLiDoThi()
        self.rules = Rules(self.qldt)

    def ve_do_thi(self):
        G = self.qldt.lay_do_thi()
        if not G.nodes(): return

        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, seed=42) # Cố định vị trí để đồ thị không nhảy lung tung

        # 1. Tạo nhãn bao gồm Tên và Giá trị (Ví dụ: "a: 5.0")
        labels = {}
        for node, attr in G.nodes(data=True):
            val = attr.get('gia_tri')
            if val is not None:
                # Nếu có giá trị thì hiển thị: Tên = Giá trị
                labels[node] = f"{node}\n({round(val, 2)})"
            else:
                labels[node] = node

        # 2. Phân loại màu sắc (Cạnh đỏ, Góc xanh, khác Vàng)
        color_map = []
        for node, attr in G.nodes(data=True):
            loai = attr.get('loai', '')
            if loai == 'canh': color_map.append('#ff7675')
            elif loai == 'goc': color_map.append('#74b9ff')
            else: color_map.append('#ffeaa7')

        # 3. Vẽ đồ thị
        nx.draw(G, pos, 
                labels=labels,           # Dùng nhãn mới có chứa giá trị
                with_labels=True, 
                node_color=color_map, 
                node_size=3000,          # Tăng kích thước node để chứa vừa chữ
                font_size=9, 
                font_weight="bold", 
                edge_color="#ced6e0",
                width=2)

        # 4. Vẽ tên công thức lên các cạnh nối (nếu bạn có thiết lập quan hệ)
        edge_labels = nx.get_edge_attributes(G, 'relation')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        plt.title("MẠNG NGỮ NGHĨA TAM GIÁC - TRẠNG THÁI HIỆN TẠI")
        plt.show()