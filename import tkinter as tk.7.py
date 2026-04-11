import tkinter as tk
from tkinter import messagebox
import math

# ================= LOGIC DEMO =================
def solve():
    result_box.delete(1.0, tk.END)
    trace_box.delete(1.0, tk.END)

    # Demo dữ liệu
    result_box.insert(tk.END, "✨ KẾT QUẢ ✨\n\n")
    result_box.insert(tk.END, "👉 a = 5.0\n👉 b = 6.0\n👉 c = 7.0\n")
    result_box.insert(tk.END, "👉 A = 44.42\n👉 B = 58.41\n👉 S = 14.7\n")

    trace_box.insert(tk.END, "🧠 SUY LUẬN\n\n")
    trace_box.insert(tk.END, "✨ c² = a² + b² - 2ab cosC\n")
    trace_box.insert(tk.END, "✨ S = 1/2 ab sinC\n")
    trace_box.insert(tk.END, "✨ a/sinA = b/sinB\n")
    trace_box.insert(tk.END, "✨ P = a + b + c\n")

def clear():
    for e in entries.values():
        e.delete(0, tk.END)
    result_box.delete(1.0, tk.END)
    trace_box.delete(1.0, tk.END)

# ================= VẼ ĐỒ THỊ (KHÔNG CẦN MATPLOTLIB) =================
def show_graph():
    graph_win = tk.Toplevel()
    graph_win.title("📊 Đồ thị sin(x)")
    graph_win.geometry("500x400")

    canvas = tk.Canvas(graph_win, bg="white")
    canvas.pack(fill="both", expand=True)

    w, h = 500, 400
    center_y = h // 2

    # trục
    canvas.create_line(0, center_y, w, center_y, fill="black")
    canvas.create_line(50, 0, 50, h, fill="black")

    # vẽ sin
    prev_x, prev_y = 50, center_y
    for i in range(0, 360):
        x = 50 + i
        y = center_y - math.sin(math.radians(i)) * 100
        canvas.create_line(prev_x, prev_y, x, y, fill="#ff6f91", width=2)
        prev_x, prev_y = x, y

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

tk.Button(btn_frame, text="📊 Graph", command=show_graph,
          bg="#4dabf7", fg="white",
          font=("Segoe UI", 11, "bold"), padx=15).grid(row=0, column=1, padx=10)

tk.Button(btn_frame, text="🧹 Clear", command=clear,
          bg="#ced4da", fg="black",
          font=("Segoe UI", 11, "bold"), padx=15).grid(row=0, column=2, padx=10)

# ===== MAIN =====
main = tk.Frame(window, bg="#f7e1ff")
main.pack(fill="both", expand=True, padx=15, pady=10)

# ===== LEFT =====
left = tk.Frame(main, bg="#f7e1ff")
left.pack(side="left", fill="both", expand=True)

# RESULT
box1 = tk.LabelFrame(left, text="✨ Kết quả ✨",
                     bg="#ffe4ec", font=("Segoe UI", 11, "bold"))
box1.pack(fill="both", expand=True, padx=5, pady=5)

scroll1 = tk.Scrollbar(box1)
scroll1.pack(side="right", fill="y")

result_box = tk.Text(box1, yscrollcommand=scroll1.set,
                     bg="white", font=("Segoe UI", 10))
result_box.pack(fill="both", expand=True)
scroll1.config(command=result_box.yview)

# TRACE
box2 = tk.LabelFrame(left, text="🧠 Suy luận ✨",
                     bg="#d0ebff", font=("Segoe UI", 11, "bold"))
box2.pack(fill="both", expand=True, padx=5, pady=5)

scroll2 = tk.Scrollbar(box2)
scroll2.pack(side="right", fill="y")

trace_box = tk.Text(box2, yscrollcommand=scroll2.set,
                    bg="white", font=("Segoe UI", 10))
trace_box.pack(fill="both", expand=True)
scroll2.config(command=trace_box.yview)

# ===== RIGHT (FORMULA) =====
right = tk.Frame(main, bg="#f7e1ff")
right.pack(side="right", fill="both", expand=True)

box3 = tk.LabelFrame(right, text="📐 20 Công Thức ✨",
                     bg="#ffe4ec", font=("Segoe UI", 11, "bold"))
box3.pack(fill="both", expand=True, padx=5, pady=5)

scroll3 = tk.Scrollbar(box3)
scroll3.pack(side="right", fill="y")

formula = tk.Text(box3,
                  yscrollcommand=scroll3.set,
                  bg="#fff0f3",
                  font=("Segoe UI", 10))
formula.pack(fill="both", expand=True)

scroll3.config(command=formula.yview)

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