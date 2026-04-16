import tkinter as tk
from tkinter import ttk, messagebox

class GiaoDienChinh:
    def __init__(self, window, controller=None):
        self.window = window
        self.controller = controller
        
        self.window.title("Triangle Expert System - Soft UI v2")
        self.window.geometry("1300x850")
        self.window.configure(bg="#f8faff")

        self.entries = {}
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        

        style.configure("Solve.TButton", font=("Segoe UI", 10, "bold"), background="#00d2d3", foreground="white", padding=12)
        style.map("Solve.TButton", background=[('active', '#01a3a4')])

        style.configure("Graph.TButton", font=("Segoe UI", 10, "bold"), background="#54a0ff", foreground="white", padding=12)
        style.map("Graph.TButton", background=[('active', '#2e86de')])

        style.configure("Clear.TButton", font=("Segoe UI", 10, "bold"), background="#ff9f43", foreground="white", padding=12)
        style.map("Clear.TButton", background=[('active', '#ee5253')])

    def create_widgets(self):
        # --- HEADER ---
        header = tk.Frame(self.window, bg="#f8faff")
        header.pack(fill="x", pady=(30, 10))
        tk.Label(header, text="Triangle Solver", font=("Helvetica", 24, "bold"), bg="#f8faff", fg="#2d3436").pack()

        container = tk.Frame(self.window, bg="#f8faff", padx=40, pady=20)
        container.pack(fill="both", expand=True)

        # --- CỘT TRÁI: INPUT ---
        left_panel = tk.Frame(container, bg="#ffffff", width=300, padx=20, pady=20)
        left_panel.pack_propagate(False)
        left_panel.pack(side="left", fill="y", padx=10)
        
        tk.Label(left_panel, text="Dữ kiện nhập", font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#2f3542").pack(anchor="w", pady=(0, 20))

        vars_to_input = [("Cạnh a", "a"), ("Cạnh b", "b"), ("Cạnh c", "c"), 
                         ("Góc A", "A"), ("Góc B", "B"), ("Góc C", "C")]

        for label, var in vars_to_input:
            tk.Label(left_panel, text=label, bg="#ffffff", fg="#57606f", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(5, 2))
            f = tk.Frame(left_panel, bg="#f1f2f6")
            f.pack(fill="x", pady=(0, 10))
            ent = tk.Entry(f, font=("Segoe UI", 11), bg="#f1f2f6", relief="flat", borderwidth=8)
            ent.pack(fill="x")
            self.entries[var] = ent

        tk.Frame(left_panel, height=20, bg="#ffffff").pack()
        ttk.Button(left_panel, text="Giải ngay", style="Solve.TButton", command=self.handle_solve).pack(fill="x", pady=5)
        ttk.Button(left_panel, text="Xem đồ thị", style="Graph.TButton", command=self.handle_draw_graph).pack(fill="x", pady=5)
        ttk.Button(left_panel, text="Làm mới", style="Clear.TButton", command=self.clear).pack(fill="x", pady=5)

        # --- CỘT PHẢI: CÔNG THỨC
        right_panel = tk.Frame(container, bg="#ffffff", width=400, padx=20, pady=20)
        right_panel.pack_propagate(False)
        right_panel.pack(side="right", fill="y", padx=10)

        tk.Label(right_panel, text="Thư viện tri thức", font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#2f3542").pack(anchor="w", pady=(0, 20))

        
        formula_text = tk.Text(right_panel, font=("Segoe UI", 10), bg="#ffffff", 
                               relief="flat", fg="#747d8c", spacing3=10) 
        formula_text.pack(fill="both", expand=True)
        
        formulas = [
            "--- Nhóm luật suy diễn hình học ---",
            "1. Kiểm tra bất đẳng thức tam giác",
            "2. Xác định Tam giác cân",
            "3.Xác định Tam giác đều",
            "4. Xác định Tam giác vuông",
            "5. Xác định Tam giác tù / Tam giác nhọn",
            "6. Xác định Tam giác vuông cân",
            "--- Nhóm công thức giải tam giác cơ bản ---",
            "7. Định lý Tổng ba góc trong một tam giác",
            "8. Định lý Pytago",
            "9. Định lý Sin",
            "10. Định lý Cosin",
            "--- Nhóm Công thức Diện tích và Chu vi ---",
            "11. Công thức tính Chu vi",
            "12. Công thức Heron",
            "13. Diện tích qua bán kính đường tròn ngoại tiếp",
            "14. Diện tích qua bán kính đường tròn nội tiếp",
            "15. Diện tích qua Sin góc xen giữa",
            "--- Nhóm Công thức Các đường đặc biệt ---",
            "16. Công thức tính Đường cao",
            "17. Công thức tính Đường trung tuyến",
            "18. Công thức tính Đường phân giác trong",
            "19. Định lý về tỉ lệ đoạn thẳng trên cạnh đáy của đường phân giác",
            "--- Nhóm Công thức Tọa độ ---",
            "20. Xác định tọa độ Tâm đường tròn ngoại tiếp",
            "21. Xác định tọa độ Tâm đường tròn nội tiếp",

        ]
        for f in formulas: formula_text.insert(tk.END, f + "\n")
        formula_text.config(state="disabled")

        # --- CỘT GIỮA: KẾT QUẢ ---
        mid_panel = tk.Frame(container, bg="#ffffff", padx=30, pady=30)
        mid_panel.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(mid_panel, text="Tiến trình giải", font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#2f3542").pack(anchor="w", pady=(0, 20))

        self.output = tk.Text(mid_panel, font=("Consolas", 11), bg="#fdfdfd", relief="flat", padx=15, pady=15, fg="#2f3542")
        self.output.pack(fill="both", expand=True)
        self.output.tag_configure("header", font=("Segoe UI", 11, "bold"), foreground="#00d2d3")

    def handle_solve(self):
        """Hàm xử lý chính khi nhấn nút Giải ngay"""
        # 1. Thu thập dữ liệu từ các ô Entry
        inputs = {k: e.get().strip() for k, e in self.entries.items() if e.get().strip()}
        
        if not inputs:
            messagebox.showwarning("Thông báo", "Vui lòng nhập ít nhất một vài dữ kiện!")
            return
        
        if self.controller:
            try:
                # 2. Reset dữ liệu cũ để tránh chồng chéo
                self.controller.reset()
                
                # 3. Chuyển dữ liệu sang Controller xử lý
                self.controller.nhap_du_lieu_ban_dau(inputs)
                self.controller.thuc_thi_suy_dien()
                
                # 4. Lấy kết quả đã định dạng từ Controller
                ket_qua = self.controller.lay_ket_qua_dinh_dang()
                vet_suy_dien = self.controller.lay_vet_suy_dien_dinh_dang()
                
                # 5. Hiển thị lên khung Text
                self.hien_thi_ket_qua(ket_qua, vet_suy_dien)
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra trong quá trình giải: {str(e)}")

    def hien_thi_ket_qua(self, ket_qua, vet_suy_dien):
        """Cập nhật văn bản vào ô kết quả"""
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        
        self.output.insert(tk.END, "=== GIÁ TRỊ TÌM ĐƯỢC ===\n", "header")
        self.output.insert(tk.END, ket_qua + "\n\n")
        
        self.output.insert(tk.END, "=== CÁC BƯỚC GIẢI CHI TIẾT ===\n", "header")
        self.output.insert(tk.END, vet_suy_dien)
        
        self.output.config(state="disabled")

    def clear(self):
        """Làm mới toàn bộ giao diện và dữ liệu"""
        for ent in self.entries.values():
            ent.delete(0, tk.END)
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.config(state="disabled")
        if self.controller:
            self.controller.reset()

    def handle_draw_graph(self):
        if self.controller:
            # Gọi hàm vẽ từ controller
            self.controller.ve_do_thi()
        else:
            messagebox.showwarning("Thông báo", "Chưa kết nối được với bộ xử lý đồ thị!")