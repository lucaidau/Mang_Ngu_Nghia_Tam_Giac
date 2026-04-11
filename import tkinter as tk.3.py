import tkinter as tk
from tkinter import messagebox
import traceback  
import math


# IMPORT MODEL
try:
    from congThuc import Rules
    from quanLiDoThi import QuanLiDoThi
except:
    pass

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

        result_box.delete(1.0, tk.END)
        trace_box.delete(1.0, tk.END)

        result_box.insert(tk.END, "🌟 KẾT QUẢ 🌟\n\n")

        for key in ["a","b","c","A","B","C","S","P"]:
            v = dt.get(key)
            if v is not None:
                result_box.insert(tk.END, f"👉 {key} = {round(v,2)}\n")

        trace_box.insert(tk.END, "🧠 SUY LUẬN\n\n")

        try:
            for edge in dt.lay_do_thi().edges(data=True):
                ct = edge[2].get("cong_thuc","")
                if ct:
                    trace_box.insert(tk.END, f"✨ {ct}\n")
        except:
            trace_box.insert(tk.END, "Chưa có suy luận 😅")

    except:
        result_box.delete(1.0, tk.END)
        result_box.insert(tk.END, traceback.format_exc())


def clear():
    for e in entries.values():
        e.delete(0, tk.END)
    result_box.delete(1.0, tk.END)
    trace_box.delete(1.0, tk.END)

# ===== VẼ ĐỒ THỊ =====
def show_graph():
    x = [i for i in range(0, 360)]
    y = [math.sin(math.radians(i)) for i in x]

    plt.figure()
    plt.plot(x, y)
    plt.title("Đồ thị sin(x)")
    plt.xlabel("Độ")
    plt.ylabel("Giá trị")
    plt.show()

# ===== HOVER =====
def hover(e): e.widget['bg'] = "#ff70a6"
def leave(e): e.widget['bg'] = "#ff4d6d"

def hover2(e): e.widget['bg'] = "#4cc9f0"
def leave2(e): e.widget['bg'] = "#4895ef"

# ================= UI =================
window = tk.Tk()
window.title("🎨 Triangle AI Pro")
window.geometry("1100x720")
window.configure(bg="#fdf0f5")

# ===== TITLE =====
tk.Label(window,
         text="🎨 TRIANGLE AI SYSTEM ✨",
         font=("Segoe UI", 20, "bold"),
         bg="#fdf0f5",
         fg="#ff4d6d").pack(pady=10)

# ===== MAIN =====
main = tk.Frame(window, bg="#fdf0f5")
main.pack(fill="both", expand=True)

# ===== INPUT =====
frame_input = tk.LabelFrame(main, text="📥 Input",
                            bg="white", font=("Segoe UI", 11, "bold"))
frame_input.pack(fill="x", padx=10, pady=5)

entries = {}
labels = ["a","b","c","A","B","C"]

for i, lb in enumerate(labels):
    tk.Label(frame_input, text=lb, bg="white").grid(row=i//3, column=(i%3)*2)
    e = tk.Entry(frame_input, width=10, bg="#fff0f3")
    e.grid(row=i//3, column=(i%3)*2+1, padx=5, pady=5)
    entries[lb] = e

# ===== BUTTON =====
btn_frame = tk.Frame(main, bg="#fdf0f5")
btn_frame.pack(pady=10)

btn1 = tk.Button(btn_frame, text="🚀 Solve", command=solve,
                 bg="#ff4d6d", fg="white", font=("Segoe UI", 11, "bold"))
btn1.grid(row=0, column=0, padx=10)

btn2 = tk.Button(btn_frame, text="📊 Graph", command=show_graph,
                 bg="#4895ef", fg="white", font=("Segoe UI", 11, "bold"))
btn2.grid(row=0, column=1, padx=10)

btn3 = tk.Button(btn_frame, text="🧹 Clear", command=clear,
                 bg="#adb5bd", fg="black", font=("Segoe UI", 11, "bold"))
btn3.grid(row=0, column=2, padx=10)

btn1.bind("<Enter>", hover)
btn1.bind("<Leave>", leave)
btn2.bind("<Enter>", hover2)
btn2.bind("<Leave>", leave2)

# ===== RESULT AREA (2 BOX) =====
frame_result = tk.Frame(main, bg="#fdf0f5")
frame_result.pack(fill="both", expand=True, padx=10)

# BOX 1
box1 = tk.LabelFrame(frame_result, text="📊 Kết quả",
                     bg="white", font=("Segoe UI", 11, "bold"))
box1.pack(side="left", fill="both", expand=True, padx=5)

result_box = tk.Text(box1, bg="#fff0f3", font=("Segoe UI", 10))
result_box.pack(fill="both", expand=True)

# BOX 2
box2 = tk.LabelFrame(frame_result, text="🧠 Suy luận",
                     bg="white", font=("Segoe UI", 11, "bold"))
box2.pack(side="right", fill="both", expand=True, padx=5)

trace_box = tk.Text(box2, bg="#f0f7ff", font=("Segoe UI", 10))
trace_box.pack(fill="both", expand=True)

# ===== FORMULA =====
frame_formula = tk.LabelFrame(main,
                              text="📐 Công thức 🔺✨",
                              bg="white",
                              font=("Segoe UI", 11, "bold"))
frame_formula.pack(fill="x", padx=10, pady=5)

formula = tk.Text(frame_formula, height=6, bg="#f8f9fa")
formula.pack(fill="both")

formula.insert(tk.END, "P=a+b+c | S=1/2 ab sinC | a²=b²+c²-2bc cosA ...")
formula.config(state=tk.DISABLED)

window.mainloop()