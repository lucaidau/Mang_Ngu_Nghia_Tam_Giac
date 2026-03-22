import tkinter as tk
from tkinter import ttk, messagebox
import traceback

# IMPORT MODEL (Đảm bảo 2 file congThuc.py và quanLiDoThi.py nằm cùng thư mục)
try:
    from app.models.congThuc import Rules
    from app.models.quanLiDoThi import QuanLiDoThi
except ImportError as e:
    print(f"LỖI KHÔNG TÌM THẤY FILE: {e}")
    print(
        "Vui lòng đảm bảo file giao diện này nằm cùng thư mục với congThuc.py và quanLiDoThi.py"
    )


def solve():
    try:
        # 1. Tạo đồ thị
        dt = QuanLiDoThi

        # 2. Gán dữ liệu từ giao diện vào model
        for key in entries:
            # Dùng strip() để xóa khoảng trắng thừa nếu người dùng bấm phím space
            val = entries[key].get().strip()
            if val:
                dt.set(key, float(val))

        # 3. Chạy Rules (Mạng ngữ nghĩa)
        rules = Rules(dt)
        rules.execute_alt()

        # 4. Hiển thị kết quả
        output.delete(1.0, tk.END)
        output.insert(tk.END, "=== KẾT QUẢ ===\n")

        keys_to_show = [
            "a",
            "b",
            "c",
            "A",
            "B",
            "C",
            "S",
            "P",
            "p",
            "R",
            "r",
            "h_a",
            "h_b",
            "h_c",
        ]
        for key in keys_to_show:
            value = dt.get(key)
            if value is not None:
                output.insert(tk.END, f"{key} = {round(value, 3)}\n")

        # 5. Hiển thị suy luận (Trace log)
        output.insert(tk.END, "\n=== VẾT SUY LUẬN (MẠNG NGỮ NGHĨA) ===\n")
        has_trace = False
        try:
            for edge in dt.lay_do_thi().edges(data=True):
                cong_thuc = edge[2].get("cong_thuc", "")
                if cong_thuc:
                    output.insert(tk.END, f"-> {cong_thuc}\n")
                    has_trace = True

            if not has_trace:
                output.insert(
                    tk.END,
                    "(Chưa có dữ liệu suy luận. Hoặc thiếu dữ kiện đầu vào, hoặc Rules chưa hoạt động)\n",
                )
        except AttributeError:
            output.insert(
                tk.END, "Lỗi: Hàm lay_do_thi() không tồn tại trong QuanLiDoThi.\n"
            )

    except ValueError:
        # Lỗi khi người dùng nhập chữ cái thay vì số
        output.delete(1.0, tk.END)
        output.insert(tk.END, "❌ Lỗi: Dữ liệu nhập vào phải là số hợp lệ!")
        messagebox.showwarning(
            "Sai định dạng", "Vui lòng chỉ nhập số vào các ô dữ kiện."
        )

    except Exception as e:
        # BẮT VÀ HIỂN THỊ LỖI THẬT SỰ TỪ THUẬT TOÁN ĐỂ DEBUG
        output.delete(1.0, tk.END)
        error_msg = traceback.format_exc()
        output.insert(
            tk.END, f"❌ LỖI HỆ THỐNG / LỖI LOGIC TỪ FILE THUẬT TOÁN:\n\n{error_msg}"
        )


def clear():
    # Xóa trắng toàn bộ ô nhập và khung kết quả
    for entry in entries.values():
        entry.delete(0, tk.END)
    output.delete(1.0, tk.END)


# ===== TẠO CỬA SỔ CHÍNH =====
window = tk.Tk()
window.title("Hệ Chuyên Gia - Giải Bài Toán Tam Giác")
window.geometry("800x700")

# ===== TIÊU ĐỀ =====
tk.Label(
    window,
    text="GIẢI BÀI TOÁN TAM GIÁC (MẠNG NGỮ NGHĨA)",
    font=("Arial", 16, "bold"),
    fg="#2c3e50",
).pack(pady=10)

# ===== KHU VỰC NHẬP LIỆU =====
frame_input = tk.LabelFrame(
    window, text="Nhập dữ kiện ban đầu (Để trống nếu không biết)", padx=10, pady=10
)
frame_input.pack(fill="x", padx=15, pady=5)

entries = {}
labels = ["a", "b", "c", "A", "B", "C"]

# Căn chỉnh lại grid cho đẹp mắt hơn
for i, label in enumerate(labels):
    tk.Label(frame_input, text=f"{label} = ", font=("Arial", 11, "bold")).grid(
        row=i // 3, column=(i % 3) * 2, padx=5, pady=10, sticky="e"
    )
    entry = tk.Entry(frame_input, width=15, font=("Arial", 11))
    entry.grid(row=i // 3, column=(i % 3) * 2 + 1, padx=15, pady=10)
    entries[label] = entry

# ===== CÁC NÚT ĐIỀU KHIỂN =====
frame_btn = tk.Frame(window)
frame_btn.pack(pady=10)

tk.Button(
    frame_btn,
    text="🚀 GIẢI BÀI TOÁN",
    width=15,
    command=solve,
    bg="#27ae60",
    fg="white",
    font=("Arial", 11, "bold"),
).grid(row=0, column=0, padx=10, ipady=3)
tk.Button(
    frame_btn,
    text="🗑️ Xóa Trắng",
    width=12,
    command=clear,
    bg="#e74c3c",
    fg="white",
    font=("Arial", 11, "bold"),
).grid(row=0, column=1, ipady=3)

# ===== KHU VỰC HIỂN THỊ KẾT QUẢ VÀ SUY LUẬN =====
frame_output = tk.LabelFrame(window, text="Kết quả & Vết suy diễn", padx=10, pady=10)
frame_output.pack(fill="both", expand=True, padx=15, pady=5)

# Thanh cuộn (Scrollbar) cho màn hình kết quả
scrollbar_out = tk.Scrollbar(frame_output)
scrollbar_out.pack(side="right", fill="y")
output = tk.Text(
    frame_output, yscrollcommand=scrollbar_out.set, font=("Consolas", 11), bg="#fdfdfd"
)
output.pack(fill="both", expand=True)
scrollbar_out.config(command=output.yview)

# ===== KHU VỰC HIỂN THỊ 20 CÔNG THỨC =====
frame_formula = tk.LabelFrame(
    window, text="Danh sách tập luật (20 Công thức)", padx=10, pady=10
)
frame_formula.pack(fill="both", padx=15, pady=5)

# Thanh cuộn cho danh sách công thức
scrollbar_form = tk.Scrollbar(frame_formula)
scrollbar_form.pack(side="right", fill="y")
formula_text = tk.Text(
    frame_formula,
    height=8,
    yscrollcommand=scrollbar_form.set,
    font=("Consolas", 10),
    bg="#f4f6f7",
)
formula_text.pack(fill="both")
scrollbar_form.config(command=formula_text.yview)

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

formula_text.insert(tk.END, danh_sach_cong_thuc)
formula_text.config(state=tk.DISABLED)  # Khóa không cho người dùng gõ sửa mất chữ

# ===== KHỞI CHẠY GIAO DIỆN =====
window.mainloop()
