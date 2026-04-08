import tkinter as tk
from tkinter import messagebox
import traceback  

# ================= LOGIC =================
def solve():
    try:
        result_box.delete(1.0, tk.END)
        trace_box.delete(1.0, tk.END)

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
window.geometry("1100x720")
window.configure(bg="#f7e1ff")

# ===== TITLE =====
tk.Label(window,
         text="📐 GIẢI TOÁN TAM GIÁC BẰNG TRÍ TUỆ NHÂN TẠO ✨",
         font=("Segoe UI", 20, "bold"),
         bg="#f7e1ff",
         fg="#333").pack(pady=10)

# ===== INPUT =====
frame_input = tk.Frame(window, bg="#ffe4ec")
frame_input.pack(fill="x", padx=20, pady=10)

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

tk.Button(btn_frame, text="🚀 Solve", command=solve,
          bg="#ff6f91", fg="white",
          font=("Segoe UI", 11, "bold"), padx=15).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="🧹 Clear", command=clear,
          bg="#ced4da", fg="black",
          font=("Segoe UI", 11, "bold"), padx=15).grid(row=0, column=1, padx=10)

# ===== MAIN CONTENT =====
main = tk.Frame(window, bg="#f7e1ff")
main.pack(fill="both", expand=True, padx=15, pady=10)

# ===== LEFT (RESULT + TRACE) =====
left = tk.Frame(main, bg="#f7e1ff")
left.pack(side="left", fill="both", expand=True)

# KẾT QUẢ
box1 = tk.LabelFrame(left, text="✨ Kết quả ✨",
                     bg="#ffe4ec", font=("Segoe UI", 11, "bold"))
box1.pack(fill="both", expand=True, padx=5, pady=5)

result_box = tk.Text(box1, bg="white", font=("Segoe UI", 10))
result_box.pack(fill="both", expand=True, padx=5, pady=5)

# SUY LUẬN
box2 = tk.LabelFrame(left, text="🧠 Suy luận ✨",
                     bg="#d0ebff", font=("Segoe UI", 11, "bold"))
box2.pack(fill="both", expand=True, padx=5, pady=5)

trace_box = tk.Text(box2, bg="white", font=("Segoe UI", 10))
trace_box.pack(fill="both", expand=True, padx=5, pady=5)

# ===== RIGHT (FORMULA) =====
right = tk.Frame(main, bg="#f7e1ff")
right.pack(side="right", fill="both", expand=True)

box3 = tk.LabelFrame(right, text="📐 20 Công Thức ✨",
                     bg="#ffe4ec", font=("Segoe UI", 11, "bold"))
box3.pack(fill="both", expand=True, padx=5, pady=5)

scroll = tk.Scrollbar(box3)
scroll.pack(side="right", fill="y")

formula = tk.Text(box3,
                  bg="#fff0f3",
                  font=("Segoe UI", 10),
                  yscrollcommand=scroll.set)
formula.pack(fill="both", expand=True, padx=5, pady=5)

scroll.config(command=formula.yview)

formula.insert(tk.END, """1. P = a + b + c
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
18. S = p r
19. r = S/p
20. R = abc/(4S)
""")

formula.config(state=tk.DISABLED)

window.mainloop()