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
        # 1. Lấy dữ liệu đồ thị từ Model
        G = self.qldt.lay_do_thi()
        
        if not G.nodes():
            print("Đồ thị trống, không có gì để vẽ.")
            return

        # 2. Khởi tạo cửa sổ vẽ
        plt.figure(figsize=(10, 7))
        plt.title("Mạng Ngữ Nghĩa Tam Giác")

        # 3. Xác định vị trí các node (Spring layout giúp các node tỏa đều)
        pos = nx.spring_layout(G, seed=42)

        # 4. Phân loại màu sắc để đồ thị đẹp hơn
        color_map = []
        for node, attr in G.nodes(data=True):
            loai = attr.get('loai', '')
            if loai == 'canh': color_map.append('#ff7675') # Màu đỏ nhạt cho cạnh
            elif loai == 'goc': color_map.append('#74b9ff') # Màu xanh cho góc
            else: color_map.append('#ffeaa7') # Màu vàng cho diện tích/chu vi

        # 5. Vẽ node và nhãn
        nx.draw(G, pos, with_labels=True, node_color=color_map, 
                node_size=2000, font_size=10, font_weight="bold", edge_color="#dfe6e9")

        # 6. Vẽ nhãn cho các quan hệ (nếu có cạnh nối)
        edge_labels = nx.get_edge_attributes(G, 'relation')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        # 7. Hiển thị
        plt.show()