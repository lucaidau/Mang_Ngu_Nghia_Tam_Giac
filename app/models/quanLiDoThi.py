import networkx as nx


class QuanLiDoThi:
    def __init__(self):
        self.G = nx.Graph()

    # --- CREATE ---
    def them_Doi_Tuong(self, ten, loai, thuoc_tinh=None):
        if thuoc_tinh == None:
            thuoc_tinh = {}
        self.G.add_node(ten, loai=loai, **thuoc_tinh)
        print(f"Đã thêm {loai} '{ten}' có {thuoc_tinh} vào đồ thị")

    def them_canh(self, u, v, quan_he):
        if self.G.has_node(u) and self.G.has_node(v):
            self.G.add_edge(u, v, relation=quan_he)
            print(f"Đã kết nối {u} và {v} với quan hệ: {quan_he}")

    # --- READ ---
    def lay_do_thi(self):
        return self.G

    def get(self, ten_doi_tuong):
        if self.G.has_node(ten_doi_tuong):
            return self.G.nodes[ten_doi_tuong].get("gia_tri")
        return 0

    # ---  UPDATE ---

    def set(self, ten, gia_tri, cong_thuc="Input"):
        if self.G.has_node(ten):
            self.G.nodes[ten]["gia_tri"] = gia_tri
            if cong_thuc != "Input":
                self.G.nodes[ten]["cong_thuc"] = cong_thuc
                self.G.nodes[ten]["gia_tri"] = gia_tri
        else:
            loai = (
                "canh"
                if ten in ["a", "b", "c"]
                else "goc" if ten in ["A", "B", "C"] else "khac"
            )
            self.them_Doi_Tuong(ten, loai, {"gia_tri": gia_tri, "cong_thuc": cong_thuc})
        print(f"-> Đã ghi nhận: {ten} = {gia_tri} ({cong_thuc})")

    # -- DELETE ---

    def xoa_node(self, ten):
        if self.G.has_node(ten):
            self.G.remove_node(ten)
            print(f"Log: Xóa Node {ten} thành công!")
        else:
            print(f"Lỗi: Node {ten} không tồn tại để xóa!")

    def xoa_canh(self, u, v):
        if self.G.has_edge(u, v):
            self.G.remove_edge(u, v)
            print(f"Log: Xóa quan hệ {u} và {v} thành công!")
        else:
            print(f"Lỗi: Quan hệ {u} và {v} không tồn tại!")
