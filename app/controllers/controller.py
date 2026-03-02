from ..models.quanLiDoThi import QuanLiDoThi
from ..views.giaoDienChinh import GiaoDienChinh


class Controller:
    def __init__(self, model: QuanLiDoThi, view: GiaoDienChinh):
        self.model = model
        self.view = view
