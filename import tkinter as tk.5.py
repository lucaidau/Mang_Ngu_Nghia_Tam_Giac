import tkinter as tk
from tkinter import messagebox
import traceback
import math

# ================= LOGIC =================
def solve():
    try:
        result_box.delete(1.0, tk.END)
        trace_box.delete(1.0, tk.END)

        # demo dữ liệu fake (bạn thay bằng model của bạn)
        result_box.insert(tk.END, "✨ KẾT QUẢ ✨\n\n")
        result_box.insert(tk.END, "👉 a = 5.0\n👉 b = 6.0\n👉 c = 7.0\n")
        result_box.insert(tk.END, "👉 A = 44.42\n👉 B = 58.41\n👉 S = 14.7\n")

        trace_box.insert(tk.END, "🧠 SUY LUẬN\n\n")
        trace_box.insert(tk.END, "✨ c² = a² + b² - 2ab cosC\n")
        trace_box.insert(tk.END, "✨ S = 1/2 ab sinC\n")
        trace_box.insert(tk.END, "✨ a/sinA = b/sinB\n")
        trace_box.insert(tk.END, "✨ P = a + b + c\n")

    except:
        result_box.insert(tk.END, traceback.format_exc())

def clear():
    for e in entries.values():
        e.delete(0, tk.END)
    result_box.delete(1.0, tk.END)
    trace_box.delete(1.0, tk.END)


# ================= UI =================
window = tk.Tk()
window.title("Triangle AI System")
window.geometry("1050x680")
window.configure(bg="#f7e1ff")

# ===== TITLE =====
tk.Label(window,
         text="📐 GIẢI TOÁN TAM GIÁC BẰNG TRÍ TUỆ NHÂN TẠO  ✨",
         font=("Segoe UI", 20, "bold"),
         bg="#f7e1ff",
         fg="#333").pack(pady=10)

# ===== INPUT CARD =====
frame_input = tk.Frame(window, bg="#ffe4ec", bd=0)
frame_input.pack(padx=20, pady=10, fill="x")

inner = tk.Frame(frame_input, bg="white")
inner.pack(padx=10, pady=10, fill="x")

entries = {}
labels = ["a","b","c","A","B","C"]

for i, lb in enumerate(labels):
    tk.Label(inner, text=f"{lb} =", bg="white",
             font=("Segoe UI",10,"bold")).grid(row=i//3, column=(i%3)*2, padx=5, pady=10)

    e = tk.Entry(inner, width=15, bg="#f9f9f9")
    e.grid(row=i//3, column=(i%3)*2+1, padx=10)
    entries[lb] = e

# ===== BUTTON =====
btn_frame = tk.Frame(window, bg="#f7e1ff")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="🚀 Solve",
          command=solve,
          bg="#ff6f91", fg="white",
          font=("Segoe UI", 11, "bold"),
          padx=15).grid(row=0, column=0, padx=10)



tk.Button(btn_frame, text="🧹 Clear",
          command=clear,
          bg="#ced4da", fg="black",
          font=("Segoe UI", 11, "bold"),
          padx=15).grid(row=0, column=2, padx=10)

# ===== RESULT AREA =====
frame_result = tk.Frame(window, bg="#f7e1ff")
frame_result.pack(fill="both", expand=True, padx=20)

# ===== LEFT BOX =====
box1 = tk.Frame(frame_result, bg="#ffe4ec")
box1.pack(side="left", fill="both", expand=True, padx=10, pady=10)

tk.Label(box1, text="✨ Kết quả ✨",
         bg="#ffe4ec",
         font=("Segoe UI", 12, "bold")).pack()

result_box = tk.Text(box1, bg="white", height=15)
result_box.pack(fill="both", expand=True, padx=10, pady=10)

# ===== RIGHT BOX =====
box2 = tk.Frame(frame_result, bg="#d0ebff")
box2.pack(side="right", fill="both", expand=True, padx=10, pady=10)

tk.Label(box2, text="🧠 Suy luận ✨",
         bg="#d0ebff",
         font=("Segoe UI", 12, "bold")).pack()

trace_box = tk.Text(box2, bg="white", height=15)
trace_box.pack(fill="both", expand=True, padx=10, pady=10)

# ===== FORMULA =====
frame_formula = tk.Frame(window, bg="#ffe4ec")
frame_formula.pack(fill="x", padx=20, pady=5)

tk.Label(frame_formula,
         text="📐 Công thức ✨ P=a+b+c | S=1/2 ab sinC",
         bg="#ffe4ec",
         font=("Segoe UI", 10)).pack(pady=5)

window.mainloop()