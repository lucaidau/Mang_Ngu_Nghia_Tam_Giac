import networkx as nx


class QuanLiDoThi:
    def __init__(self):
        self.G = nx.Graph()

    def them_Doi_Tuong(self, ten, loai, thuoc_tinh=None):
        if thuoc_tinh == None:
            thuoc_tinh = {}
        self.G.add_node(ten, loai=loai, **thuoc_tinh)

    def them_quan_he(self, u, v, quan_he):
        self.G.add_edge(u, v, relation=quan_he)

    def lay_do_thi(self):
        return self.G
