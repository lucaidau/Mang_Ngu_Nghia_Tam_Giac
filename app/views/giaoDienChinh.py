import tkinter as tk
from tkinter import ttk, messagebox


class GiaoDienChinh:
    def __init__(self, window, controller):
        self.window = window
        self.controller = controller
        self.title = "Hệ Chuyên Gia - Giải Bài Toán Tam Giác"
        self.geometry = "800x700"

        self.entries = {}
        self.giaoDien()

        self.lbl_status = tk.Label(
            self.window, text="Sẵn sàng", bd=1, relief=tk.SUNKEN, anchor=tk.W
        )
        self.lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

    def giaoDien(self):
        tk.Label(
            self.window,
            text="GIẢI BÀI TOÁN TAM GIÁC (MẠNG NGỮ NGHĨA)",
            font=("Arial", 16, "bold"),
            fg="#2c3e50",
        ).pack(pady=10)

        # ===== KHU VỰC NHẬP LIỆU =====
        frame_input = tk.LabelFrame(
            self.window,
            text="Nhập dữ kiện ban đầu (Để trống nếu không biết)",
            padx=10,
            pady=10,
        )
        frame_input.pack(fill="x", padx=15, pady=5)

        labels = ["a", "b", "c", "A", "B", "C"]

        # Căn chỉnh lại grid cho đẹp mắt hơn
        for i, label in enumerate(labels):
            tk.Label(frame_input, text=f"{label} = ", font=("Arial", 11, "bold")).grid(
                row=i // 3, column=(i % 3) * 2, padx=5, pady=10, sticky="e"
            )
            entry = tk.Entry(frame_input, width=15, font=("Arial", 11))
            entry.grid(row=i // 3, column=(i % 3) * 2 + 1, padx=15, pady=10)
            self.entries[label] = entry

        # ===== CÁC NÚT ĐIỀU KHIỂN =====
        frame_btn = tk.Frame(self.window)
        frame_btn.pack(pady=10)

        tk.Button(
            frame_btn,
            text="🚀 GIẢI BÀI TOÁN",
            width=15,
            command=self.handle_solve,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
        ).grid(row=0, column=0, padx=10, ipady=3)
        tk.Button(
            frame_btn,
            text="🗑️ Xóa Trắng",
            width=12,
            command=self.clear,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 11, "bold"),
        ).grid(row=0, column=1, ipady=3)

        # ===== KHU VỰC HIỂN THỊ KẾT QUẢ VÀ SUY LUẬN =====
        frame_output = tk.LabelFrame(
            self.window, text="Kết quả & Vết suy diễn", padx=10, pady=10
        )
        frame_output.pack(fill="both", expand=True, padx=15, pady=5)

        # Thanh cuộn (Scrollbar) cho màn hình kết quả
        self.scrollbar_out = tk.Scrollbar(frame_output)
        self.scrollbar_out.pack(side="right", fill="y")
        self.output = tk.Text(
            frame_output,
            yscrollcommand=self.scrollbar_out.set,
            font=("Consolas", 11),
            bg="#fdfdfd",
        )
        self.output.pack(fill="both", expand=True)
        self.scrollbar_out.config(command=self.output.yview)

        # ===== KHU VỰC HIỂN THỊ 20 CÔNG THỨC =====
        frame_formula = tk.LabelFrame(
            self.window, text="Danh sách tập luật (20 Công thức)", padx=10, pady=10
        )
        frame_formula.pack(fill="both", padx=15, pady=5)

        # Thanh cuộn cho danh sách công thức
        self.scrollbar_form = tk.Scrollbar(frame_formula)
        self.scrollbar_form.pack(side="right", fill="y")
        self.formula_text = tk.Text(
            frame_formula,
            height=8,
            yscrollcommand=self.scrollbar_form.set,
            font=("Consolas", 10),
            bg="#f4f6f7",
        )
        self.formula_text.pack(fill="both")
        self.scrollbar_form.config(command=self.formula_text.yview)

        # Chèn danh sách công thức
        danh_sach_cong_thuc = """1. P = a + b + c
        2. p = (a + b + c)/2
        3. S = √(p(p-a)(p-b)(p-c)) (Heron)
        4. S = 1/2 ab sinC
        5. S = 1/2 bc sinA
        6. S = 1/2 ca sinB
        7. a² = b² + c² - 2bc cosA
        8. b² = a² + c² - 2ac cosB
        9. c² = a² + b² - 2ab cosC
        10. a/sinA = b/sinB = c/sinC = 2R
        11. R = a/(2sinA)
        12. Tổng góc: A + B + C = 180°
        13. Trung tuyến: ma = 1/2√(2b² + 2c² - a²)
        14. Tam giác đều: a = b = c
        15. Tam giác cân: a = b
        16. Tam giác vuông: a² + b² = c²
        17. Đường cao: S = 1/2 * a * ha
        18. Chu vi nội tiếp: S = pr
        19. Bán kính nội tiếp: r = S/p
        20. Bán kính ngoại tiếp: R = abc/(4S)"""

        self.formula_text.insert(tk.END, danh_sach_cong_thuc)
        self.formula_text.config(
            state=tk.DISABLED
        )  # Khóa không cho người dùng gõ sửa mất chữ

    def handle_solve(self):
        if not self.controller:
            messagebox.showerror("Lỗi", "Controller chưa được kết nối")
            return

        inputs = {key: entry.get().strip() for key, entry in self.entries.items()}
        self.controller.reset()
        self.controller.nhap_du_lieu_ban_dau(inputs)
        self.controller.thuc_thi_suy_dien()

        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, self.controller.lay_ket_qua_dinh_dang())
        self.output.insert(
            tk.END, "\n\n" + self.controller.lay_vet_suy_dien_dinh_dang()
        )

    def clear(self):
        # Xóa trắng toàn bộ ô nhập và khung kết quả
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.output.delete(1.0, tk.END)
        if self.controller:
            self.controller.reset()

    def hien_thi_trang_thai(self, message):
        self.lbl_status.config(text=message)
