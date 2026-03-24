from ..models.quanLiDoThi import QuanLiDoThi
from ..views.giaoDienChinh import GiaoDienChinh
from ..models.congThuc import Rules


class Controller:
    def __init__(self, view: GiaoDienChinh = None):
        """
        Khởi tạo controller.
        - view: tham chiếu đến giao diện (để gọi các hàm cập nhật UI nếu cần)
        """
        self.view = view
        self.qldt = QuanLiDoThi()
        self.rules = Rules(self.qldt)
        self._status_message = ""

    def set_view(self, view: GiaoDienChinh):
        """Gán view sau nếu chưa có lúc init"""
        self.view = view

    def nhap_du_lieu_ban_dau(self, data_dict: dict):
        """
        Nhận dữ liệu từ view (dict key-value) và thêm vào đồ thị.
        - key là tên biến (a, b, c, A, B, C, ...)
        - value là số thực (float/int)
        """
        self._status_message = "Đang nạp dữ liệu đầu vào..."
        if self.view:
            self.view.hien_thi_trang_thai(self._status_message)

        print("--- Đang nạp dữ liệu đầu vào ---")
        for key, value in data_dict.items():
            if value is None or value == "":
                continue

            try:
                gia_tri = float(value)
            except (ValueError, TypeError):
                print(f"Cảnh báo: Giá trị '{value}' của {key} không phải số → bỏ qua")
                continue

            # Xác định loại đối tượng dựa trên quy ước tên biến
            if key in ['a', 'b', 'c']:
                loai = "canh"
            elif key in ['A', 'B', 'C']:
                loai = "goc"
            elif key in ['S', 'P', 'p', 'R', 'r', 'h_a', 'm_a', 'l_a']:
                loai = "thong_so_khac"
            else:
                loai = "khac"

            # Thêm node nếu chưa tồn tại hoặc cập nhật giá trị
            if self.qldt.get(key) is None:
                self.qldt.them_node(key, loai, {
                    "gia_tri": gia_tri,
                    "cong_thuc": "Dữ liệu đầu vào từ người dùng"
                })
            else:
                self.qldt.set(key, gia_tri)

        print("→ Đã nạp xong dữ liệu đầu vào")
        self._status_message = f"Đã nạp {len(data_dict)} dữ kiện ban đầu"
        if self.view:
            self.view.hien_thi_trang_thai(self._status_message)

    def thuc_thi_suy_dien(self):
        """Kích hoạt toàn bộ bộ suy diễn luật (execute_alt)"""
        self._status_message = "Đang chạy suy diễn mạng ngữ nghĩa..."
        if self.view:
            self.view.hien_thi_trang_thai(self._status_message)

        print("\n--- Bắt đầu quá trình giải toán ---")
        self.rules.execute_alt()
        print("--- Quá trình giải hoàn tất ---\n")

        self._status_message = "Suy diễn hoàn tất"
        if self.view:
            self.view.hien_thi_trang_thai(self._status_message)

    def lay_ket_qua(self) -> dict:
        """Trả về dict tất cả các node có giá trị (dùng cho view hiển thị)"""
        graph = self.qldt.lay_do_thi()
        ket_qua = {}
        for node, attr in graph.nodes(data=True):
            val = attr.get('gia_tri')
            if val is not None:
                ket_qua[node] = val
        return ket_qua

    def lay_ket_qua_dinh_dang(self) -> str:
        """
        Trả về chuỗi văn bản đã định dạng đẹp để hiển thị trực tiếp lên Text widget
        """
        ket_qua = self.lay_ket_qua()
        if not ket_qua:
            return "Chưa suy ra được giá trị nào.\nHãy nhập thêm dữ kiện."

        lines = ["=== KẾT QUẢ ==="]
        for key in sorted(ket_qua.keys()):
            val = ket_qua[key]
            if isinstance(val, (int, float)):
                lines.append(f"{key:>4} = {val:.4f}")
            else:
                lines.append(f"{key:>4} = {val}")
        return "\n".join(lines)

    def lay_vet_suy_dien(self) -> list:
        """
        Trả về danh sách các dòng vết suy diễn (dùng để hiển thị phần trace)
        """
        graph = self.qldt.lay_do_thi()
        traces = []

        # Duyệt các cạnh có thuộc tính cong_thuc
        for u, v, data in graph.edges(data=True):
            cong_thuc = data.get('cong_thuc', '').strip()
            if cong_thuc:
                gia_tri_u = graph.nodes[u].get('gia_tri')
                gia_tri_v = graph.nodes[v].get('gia_tri')
                line = f"{u} → {v} : {cong_thuc}"
                if gia_tri_v is not None:
                    line += f"  →  {v} = {gia_tri_v:.4f}"
                traces.append(line)

        if not traces:
            traces.append("(Chưa có quy tắc nào được kích hoạt hoặc chưa lưu cong_thuc vào cạnh)")

        return traces

    def lay_vet_suy_dien_dinh_dang(self) -> str:
        """Chuỗi văn bản đầy đủ cho phần vết suy diễn"""
        traces = self.lay_vet_suy_dien()
        return "\n".join(["=== VẾT SUY LUẬN ==="] + traces)

    def reset(self):
        """Xóa toàn bộ dữ liệu để bắt đầu bài toán mới"""
        self.qldt = QuanLiDoThi()
        self.rules = Rules(self.qldt)
        self._status_message = "Đã reset – sẵn sàng cho bài toán mới"
        if self.view:
            self.view.hien_thi_trang_thai(self._status_message)

    def thong_tin_trang_thai(self) -> str:
        """Trả về thông tin trạng thái hiện tại (số node, số cạnh, v.v.)"""
        graph = self.qldt.lay_do_thi()
        return f"Nodes: {graph.number_of_nodes()} | Edges: {graph.number_of_edges()}"


# --- Test nhanh (console) ---
if __name__ == "__main__":
    controller = Controller()

    # Ví dụ dữ liệu từ người dùng
    du_lieu = {
        'a': 6,
        'b': 8,
        'C': 90,        # tam giác vuông
        # 'A': 30,      # thử thêm nếu muốn
    }

    controller.nhap_du_lieu_ban_dau(du_lieu)
    controller.thuc_thi_suy_dien()

    print(controller.lay_ket_qua_dinh_dang())
    print("\n" + controller.lay_vet_suy_dien_dinh_dang())