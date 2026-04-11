import tkinter as tk
from tkinter import ttk, messagebox
import traceback  
# IMPORT MODEL
try:
    from congThuc import Rules
    from quanLiDoThi import QuanLiDoThi
except ImportError as e:
    print(f"LỖI KHÔNG TÌM THẤY FILE: {e}")

# ================== LOGIC ==================
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
        output.insert(tk.END, "=== KẾT QUẢ ===\n\n")

        keys_to_show = ["a", "b", "c", "A", "B", "C", "S", "P", "p", "R", "r", "h_a", "h_b", "h_c"]
        for key in keys_to_show:
            value = dt.get(key)
            if value is not None:
                output.insert(tk.END, f"{key} = {round(value, 3)}\n")
        output.insert(tk.END, "\n=== SUY LUẬN ===\n\n")
        try:
            for edge in dt.lay_do_thi().edges(data=True):
                cong_thuc = edge[2].get("cong_thuc", "")
                if cong_thuc:
                    output.insert(tk.END, f"→ {cong_thuc}\n")
        except:
            output.insert(tk.END, "Không có dữ liệu suy luận.\n")

    except ValueError:
        messagebox.showwarning("Lỗi", "Chỉ nhập số!")
    except Exception:
        output.delete(1.0, tk.END)
        output.insert(tk.END, traceback.format_exc())
def clear():
    for entry in entries.values():
        entry.delete(0, tk.END)
    output.delete(1.0, tk.END)


# ================== UI ==================
window = tk.Tk()
window.title("🧠 Semantic Network - Giải Tam Giác")
window.geometry("1000x700")
window.configure(bg="#0f172a")
# TITLE
tk.Label(window,
         text="🧠 HỆ CHUYÊN GIA TAM GIÁC",
         font=("Segoe UI", 18, "bold"),
         fg="#38bdf8", bg="#0f172a").pack(pady=10)
tk.Label(window,
         text="Giải bằng mạng ngữ nghĩa - AI System",
         font=("Segoe UI", 10),
         fg="#94a3b8", bg="#0f172a").pack()
# MAIN LAYOUT
main_frame = tk.Frame(window, bg="#0f172a")
main_frame.pack(fill="both", expand=True, pady=10)
left_frame = tk.Frame(main_frame, bg="#0f172a")
left_frame.pack(side="left", fill="both", expand=True, padx=10)
right_frame = tk.Frame(main_frame, bg="#0f172a")
right_frame.pack(side="right", fill="y", padx=10)
# ===== INPUT =====
frame_input = tk.LabelFrame(left_frame,
                            text="📥 Dữ kiện đầu vào",
                            bg="#1e293b",
                            fg="white",
                            font=("Segoe UI", 11, "bold"),
                            padx=10, pady=10)
frame_input.pack(fill="x", pady=5)
entries = {}
labels = ["a", "b", "c", "A", "B", "C"]
for i, label in enumerate(labels):
    tk.Label(frame_input, text=f"{label} =",
             bg="#1e293b", fg="white",
             font=("Segoe UI", 11, "bold")
             ).grid(row=i//3, column=(i%3)*2, padx=5, pady=10)
    entry = tk.Entry(frame_input,
                     width=15,
                     font=("Segoe UI", 11),
                     bg="#334155",
                     fg="white",
                     insertbackground="white",
                     relief="flat")
    entry.grid(row=i//3, column=(i%3)*2 + 1, padx=10)
    entries[label] = entry
# ===== BUTTON =====
frame_btn = tk.Frame(left_frame, bg="#0f172a")
frame_btn.pack(pady=10)
tk.Button(frame_btn, text="🚀 Giải",
          command=solve,
          bg="#22c55e",
          fg="white",
          font=("Segoe UI", 11, "bold"),
          relief="flat",
          padx=10).grid(row=0, column=0, padx=10)
tk.Button(frame_btn, text="🗑️ Xóa",
          command=clear,
          bg="#ef4444",
          fg="white",
          font=("Segoe UI", 11, "bold"),
          relief="flat",
          padx=10).grid(row=0, column=1)
# ===== OUTPUT =====
frame_output = tk.LabelFrame(left_frame,
                             text="📊 Kết quả & Suy luận",
                             bg="#1e293b",
                             fg="white",
                             font=("Segoe UI", 11, "bold"),
                             padx=10, pady=10)
frame_output.pack(fill="both", expand=True)
scrollbar = tk.Scrollbar(frame_output)
scrollbar.pack(side="right", fill="y")
output = tk.Text(frame_output,
                 yscrollcommand=scrollbar.set,
                 font=("Consolas", 11),
                 bg="#020617",
                 fg="#22c55e",
                 insertbackground="white")
output.pack(fill="both", expand=True)
scrollbar.config(command=output.yview)
# ===== FORMULA SIDEBAR =====
frame_formula = tk.LabelFrame(right_frame,
                              text="📐 20 Công Thức",
                              bg="#1e293b",
                              fg="white",
                              font=("Segoe UI", 11, "bold"),
                              padx=10, pady=10)
frame_formula.pack(fill="both", expand=True)

scrollbar_f = tk.Scrollbar(frame_formula)
scrollbar_f.pack(side="right", fill="y")
formula_text = tk.Text(frame_formula,
                       height=30,
                       yscrollcommand=scrollbar_f.set,
                       font=("Consolas", 10),
                       bg="#020617",
                       fg="#38bdf8")
formula_text.pack(fill="both")
scrollbar_f.config(command=formula_text.yview)
formula_text.insert(tk.END, """1. P = a + b + c
2. p = (a + b + c)/2
3. S = √(p(p-a)(p-b)(p-c))
4. S = 1/2 ab sinC
5. S = 1/2 bc sinA
6. S = 1/2 ca sinB
7. a² = b² + c² - 2bc cosA
8. b² = a² + c² - 2ac cosB
9. c² = a² + b² - 2ab cosC
10. a/sinA = b/sinB = c/sinC = 2R
11. R = a/(2sinA)
12. A + B + C = 180°
13. ma = 1/2√(2b² + 2c² - a²)
14. a = b = c
15. a = b
16. a² + b² = c²
17. S = 1/2 a ha
18. S = pr
19. r = S/p
20. R = abc/(4S)""")
formula_text.config(state=tk.DISABLED)
# CHẠY 
window.mainloop()
