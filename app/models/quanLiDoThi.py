import networkx as nx


class QuanLiDoThi:
    def __init__(self):
        self.G = nx.Graph()

    # --- CREATE ---
    def them_node(self, ten, loai, thuoc_tinh=None):
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

    def lay_gia_tri_node(self, ten_doi_tuong):
        if self.G.has_node(ten_doi_tuong):
            return self.G.nodes[ten_doi_tuong].get("gia_tri")
        return None

    def lay_tat_ca_node_theo_loai(self, loai_can_tim):
        ket_qua = []
        for node, data in self.G.nodes(data=True):
            if data.get("loai") == loai_can_tim:
                ket_qua.append(node)
        return ket_qua

    def lay_thong_tin_canh(self, u, v):
        if self.G.has_edge(u, v):
            return self.G.edges[u, v]
        return None

    def lay_tat_ca_canh_cua_node(self, u):
        return list(self.G.edges(u, data=True))

    # ---  UPDATE ---
    def cap_nhat_node(self, ten, thuoc_tinh_moi):
        if self.G.has_node(ten):
            self.G.nodes[ten].update(thuoc_tinh_moi)
            print(f"Log: Đã cập nhật Node {ten} thành công!")
        else:
            print(f"Lỗi: Node {ten} không tồn tại để cập nhật!")

    def cap_nhat_canh(self, u, v, quan_he_moi):
        if self.G.has_edge(u, v):
            self.G.edges[u, v]["quan_he"] = quan_he_moi
        else:
            self.them_canh(u, v, quan_he_moi)

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
