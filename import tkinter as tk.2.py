import tkinter as tk
from tkinter import messagebox
import traceback  

# IMPORT MODEL
try:
    from congThuc import Rules
    from quanLiDoThi import QuanLiDoThi
except ImportError as e:
    print(f"LỖI: {e}")

# ================= LOGIC =================
def solve():
    try:
        dt = QuanLiDoThi()

        for key in entries:
            val = entries[key].get().strip()
            if val:
                dt.set(key, float(val))

        rules = Rules(dt)
        rules.execute_alt()

        output.delete(1.0, tk.END)
        output.insert(tk.END, "🌟 KẾT QUẢ 🌟\n\n")

        keys = ["a", "b", "c", "A", "B", "C", "S", "P", "p", "R", "r"]
        for key in keys:
            value = dt.get(key)
            if value is not None:
                output.insert(tk.END, f"👉 {key} = {round(value,2)}\n")

        output.insert(tk.END, "\n🧠 SUY LUẬN:\n\n")

        try:
            for edge in dt.lay_do_thi().edges(data=True):
                ct = edge[2].get("cong_thuc", "")
                if ct:
                    output.insert(tk.END, f"✨ {ct}\n")
        except:
            output.insert(tk.END, "Chưa có suy luận 😅")

    except:
        output.delete(1.0, tk.END)
        output.insert(tk.END, traceback.format_exc())

def clear():
    for e in entries.values():
        e.delete(0, tk.END)
    output.delete(1.0, tk.END)

# ================= UI =================
window = tk.Tk()
window.title("📐 Học Tam Giác Thông Minh")
window.geometry("1000x700")
window.configure(bg="#eaf7f6")  # nền dịu

# ===== TITLE =====
tk.Label(window,
         text="📐 HỌC TAM GIÁC THÔNG MINH",
         font=("Segoe UI", 18, "bold"),
         bg="#eaf7f6",
         fg="#2a7f62").pack(pady=10)

tk.Label(window,
         text="Học vui với AI - Mạng ngữ nghĩa 🧠",
         font=("Segoe UI", 10),
         bg="#eaf7f6",
         fg="#5c7c77").pack()

# ===== MAIN =====
main = tk.Frame(window, bg="#eaf7f6")
main.pack(fill="both", expand=True)

left = tk.Frame(main, bg="#eaf7f6")
left.pack(side="left", fill="both", expand=True, padx=10)

right = tk.Frame(main, bg="#eaf7f6")
right.pack(side="right", fill="y", padx=10)

# ===== INPUT =====
frame_input = tk.LabelFrame(left,
                            text="📥 Nhập dữ kiện",
                            bg="#ffffff",
                            fg="#2a7f62",
                            font=("Segoe UI", 11, "bold"),
                            padx=10, pady=10)
frame_input.pack(fill="x", pady=5)

entries = {}
labels = ["a", "b", "c", "A", "B", "C"]

for i, lb in enumerate(labels):
    tk.Label(frame_input,
             text=f"{lb} =",
             bg="white",
             fg="#333",
             font=("Segoe UI", 11, "bold")
             ).grid(row=i//3, column=(i%3)*2, padx=5, pady=10)

    e = tk.Entry(frame_input,
                 width=15,
                 font=("Segoe UI", 11),
                 bg="#f4fbfb",
                 relief="solid",
                 bd=1)
    e.grid(row=i//3, column=(i%3)*2+1, padx=10)
    entries[lb] = e

# ===== BUTTON =====
btn_frame = tk.Frame(left, bg="#eaf7f6")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="🚀 Giải",
          command=solve,
          bg="#6bcf9b",
          fg="white",
          font=("Segoe UI", 11, "bold"),
          relief="flat",
          padx=12).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="🧹 Xóa",
          command=clear,
          bg="#ff8fa3",
          fg="white",
          font=("Segoe UI", 11, "bold"),
          relief="flat",
          padx=12).grid(row=0, column=1)

# ===== OUTPUT =====
frame_out = tk.LabelFrame(left,
                          text="📊 Kết quả",
                          bg="white",
                          fg="#2a7f62",
                          font=("Segoe UI", 11, "bold"),
                          padx=10, pady=10)
frame_out.pack(fill="both", expand=True)

output = tk.Text(frame_out,
                 font=("Segoe UI", 11),
                 bg="#f8fdfd",
                 fg="#333")
output.pack(fill="both", expand=True)

# ===== FORMULA =====
frame_formula = tk.LabelFrame(right,
                              text="📐 Công thức",
                              bg="white",
                              fg="#2a7f62",
                              font=("Segoe UI", 11, "bold"),
                              padx=10, pady=10)
frame_formula.pack(fill="both", expand=True)

formula = tk.Text(frame_formula,
                  font=("Segoe UI", 10),
                  bg="#f8fdfd",
                  fg="#333")
formula.pack(fill="both", expand=True)

formula.insert(tk.END, """📐 20 Công Thức

1. P = a + b + c
2. p = (a + b + c)/2
3. S = √(p(p-a)(p-b)(p-c))
4. S = 1/2 ab sinC
5. S = 1/2 bc sinA
6. S = 1/2 ca sinB
7. a² = b² + c² - 2bc cosA
8. b² = a² + c² - 2ac cosB
9. c² = a² + b² - 2ab cosC
10. a/sinA = b/sinB = c/sinC
...
""")

formula.config(state=tk.DISABLED)

window.mainloop()