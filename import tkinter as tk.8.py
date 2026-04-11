import tkinter as tk
from tkinter import messagebox
import traceback

# THƯ VIỆN VẼ ĐỒ THỊ
import matplotlib.pyplot as plt
import networkx as nx

# IMPORT MODEL
try:
    from congThuc import Rules
    from quanLiDoThi import QuanLiDoThi
except:
    pass


# ================= SOLVE =================
def solve():
    try:
        dt = QuanLiDoThi()

        # lấy input
        for key in entries:
            val = entries[key].get().strip()
            if val:
                dt.set(key, float(val))

        # chạy suy luận
        rules = Rules(dt)
        rules.execute_alt()

        # HIỂN THỊ KẾT QUẢ
        result_box.delete(1.0, tk.END)
        result_box.insert(tk.END, "✨ KẾT QUẢ ✨\n\n")

        for key in ["a","b","c","A","B","C","S","P","p","R","r"]:
            v = dt.get(key)
            if v is not None:
                result_box.insert(tk.END, f"👉 {key} = {round(v,3)}\n")

        # HIỂN THỊ SUY LUẬN
        trace_box.delete(1.0, tk.END)
        trace_box.insert(tk.END, "🧠 SUY LUẬN\n\n")

        has_trace = False
        try:
            for edge in dt.lay_do_thi().edges(data=True):
                ct = edge[2].get("cong_thuc","")
                if ct:
                    trace_box.insert(tk.END, f"✨ {ct}\n")
                    has_trace = True

            if not has_trace:
                trace_box.insert(tk.END, "Chưa có suy luận 😅")

        except:
            trace_box.insert(tk.END, "Không lấy được dữ liệu đồ thị")

    except Exception as e:
        result_box.delete(1.0, tk.END)
        result_box.insert(tk.END, traceback.format_exc())


# ================= GRAPH =================
def show_graph():
    try:
        dt = QuanLiDoThi()

        for key in entries:
            val = entries[key].get().strip()
            if val:
                dt.set(key, float(val))

        rules = Rules(dt)
        rules.execute_alt()

        g = dt.lay_do_thi()

        G = nx.DiGraph()

        for u, v, data in g.edges(data=True):
            label = data.get("cong_thuc", "")
            G.add_edge(u, v, label=label)

        pos = nx.spring_layout(G)

        plt.figure()
        nx.draw(G, pos,
                with_labels=True,
                node_size=2000)

        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos,
                                     edge_labels=edge_labels,
                                     font_size=8)

        plt.title("Mạng ngữ nghĩa suy luận tam giác")
        plt.show()

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


# ================= CLEAR =================
def clear():
    for e in entries.values():
        e.delete(0, tk.END)
    result_box.delete(1.0, tk.END)
    trace_box.delete(1.0, tk.END)


# ================= UI =================
window = tk.Tk()
window.title("Hệ chuyên gia giải bài toán tam giác")
window.geometry("1100x720")
window.configure(bg="#f7e1ff")

# TITLE
tk.Label(window,
         text="📐 HỆ CHUYÊN GIA GIẢI TAM GIÁC ✨",
         font=("Segoe UI", 20, "bold"),
         bg="#f7e1ff",
         fg="#333").pack(pady=10)

# INPUT
frame_input = tk.Frame(window, bg="#ffe4ec")
frame_input.pack(fill="x", padx=20, pady=10)

inner = tk.Frame(frame_input, bg="white")
inner.pack(padx=10, pady=10, fill="x")

entries = {}
labels = ["a","b","c","A","B","C"]

for i, lb in enumerate(labels):
    tk.Label(inner, text=f"{lb} =", bg="white",
             font=("Segoe UI",10,"bold")).grid(row=i//3, column=(i%3)*2)

    e = tk.Entry(inner, width=15)
    e.grid(row=i//3, column=(i%3)*2+1, padx=10, pady=5)
    entries[lb] = e

# BUTTON
btn_frame = tk.Frame(window, bg="#f7e1ff")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="🚀 Solve", command=solve,
          bg="#ff6f91", fg="white",
          font=("Segoe UI", 11, "bold")).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="📊 Xem đồ thị", command=show_graph,
          bg="#4dabf7", fg="white",
          font=("Segoe UI", 11, "bold")).grid(row=0, column=1, padx=10)

tk.Button(btn_frame, text="🧹 Clear", command=clear,
          bg="#ced4da", fg="black",
          font=("Segoe UI", 11, "bold")).grid(row=0, column=2, padx=10)

# MAIN
main = tk.Frame(window, bg="#f7e1ff")
main.pack(fill="both", expand=True, padx=15, pady=10)

# LEFT
left = tk.Frame(main, bg="#f7e1ff")
left.pack(side="left", fill="both", expand=True)

# RESULT
box1 = tk.LabelFrame(left, text="✨ Kết quả ✨",
                     bg="#ffe4ec", font=("Segoe UI", 11, "bold"))
box1.pack(fill="both", expand=True, padx=5, pady=5)

result_box = tk.Text(box1)
result_box.pack(fill="both", expand=True)

# TRACE
box2 = tk.LabelFrame(left, text="🧠 Suy luận ✨",
                     bg="#d0ebff", font=("Segoe UI", 11, "bold"))
box2.pack(fill="both", expand=True, padx=5, pady=5)

trace_box = tk.Text(box2)
trace_box.pack(fill="both", expand=True)

# RIGHT (FORMULA)
right = tk.Frame(main, bg="#f7e1ff")
right.pack(side="right", fill="both", expand=True)

box3 = tk.LabelFrame(right, text="📐 20 Công Thức ✨",
                     bg="#ffe4ec", font=("Segoe UI", 11, "bold"))
box3.pack(fill="both", expand=True, padx=5, pady=5)

formula = tk.Text(box3, bg="#fff0f3")
formula.pack(fill="both", expand=True)

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