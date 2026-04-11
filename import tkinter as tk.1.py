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

        output.insert(tk.END, "🌟 KẾT QUẢ 🌟\n\n", "title")

        keys = ["a", "b", "c", "A", "B", "C", "S", "P", "p", "R", "r"]

        for key in keys:
            value = dt.get(key)
            if value is not None:
                output.insert(tk.END, f"👉 {key} = {round(value,2)}\n", "highlight")

        output.insert(tk.END, "\n🧠 SUY LUẬN:\n\n", "brain")

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

# ===== HOVER EFFECT =====
def hover_green(e):
    e.widget['bg'] = "#52b788"

def leave_green(e):
    e.widget['bg'] = "#74c69d"

def hover_pink(e):
    e.widget['bg'] = "#ff758f"

def leave_pink(e):
    e.widget['bg'] = "#ff8fa3"

# ================= UI =================
window = tk.Tk()
window.title("📐 Học Tam Giác Thông Minh")
window.geometry("1000x700")
window.configure(bg="#edf6f9")

# ===== BACKGROUND DECOR =====
bg_canvas = tk.Canvas(window, bg="#edf6f9", highlightthickness=0)
bg_canvas.place(relwidth=1, relheight=1)

bg_canvas.create_text(120, 100, text="📐", font=("Segoe UI Emoji", 28), fill="#d0ebea")
bg_canvas.create_text(850, 120, text="🔺", font=("Segoe UI Emoji", 26), fill="#d0ebea")
bg_canvas.create_text(200, 600, text="📏", font=("Segoe UI Emoji", 26), fill="#d0ebea")
bg_canvas.create_text(800, 500, text="✨", font=("Segoe UI Emoji", 26), fill="#d0ebea")
bg_canvas.create_text(500, 350, text="🧠", font=("Segoe UI Emoji", 24), fill="#e0f2f1")

# ===== MAIN =====
main = tk.Frame(window, bg="#edf6f9")
main.place(relwidth=1, relheight=1)

# ===== TITLE =====
tk.Label(main,
         text="📐 HỌC TAM GIÁC THÔNG MINH",
         font=("Segoe UI", 18, "bold"),
         bg="#edf6f9",
         fg="#1d3557").pack(pady=10)

tk.Label(main,
         text="Học vui với AI - Mạng ngữ nghĩa 🧠",
         font=("Segoe UI", 10),
         bg="#edf6f9",
         fg="#6c757d").pack()

# ===== LAYOUT =====
content = tk.Frame(main, bg="#edf6f9")
content.pack(fill="both", expand=True)

left = tk.Frame(content, bg="#edf6f9")
left.pack(side="left", fill="both", expand=True, padx=10)

right = tk.Frame(content, bg="#edf6f9")
right.pack(side="right", fill="y", padx=10)

# ===== INPUT =====
frame_input = tk.LabelFrame(left,
                            text="📥 Nhập dữ kiện",
                            bg="white",
                            fg="#1d3557",
                            font=("Segoe UI", 11, "bold"),
                            padx=10, pady=10)
frame_input.pack(fill="x", pady=5)

entries = {}
labels = ["a", "b", "c", "A", "B", "C"]

for i, lb in enumerate(labels):
    tk.Label(frame_input,
             text=f"{lb} =",
             bg="white",
             font=("Segoe UI", 11, "bold")
             ).grid(row=i//3, column=(i%3)*2, padx=5, pady=10)

    e = tk.Entry(frame_input,
                 width=15,
                 font=("Segoe UI", 11),
                 bg="#ffffff",
                 relief="flat",
                 highlightthickness=2,
                 highlightbackground="#cce3de",
                 highlightcolor="#74c69d")
    e.grid(row=i//3, column=(i%3)*2+1, padx=10)
    entries[lb] = e

# ===== BUTTON =====
btn_frame = tk.Frame(left, bg="#edf6f9")
btn_frame.pack(pady=10)

btn_solve = tk.Button(btn_frame, text="🚀 Giải",
                      command=solve,
                      bg="#74c69d",
                      fg="white",
                      font=("Segoe UI", 11, "bold"),
                      relief="flat",
                      padx=12)
btn_solve.grid(row=0, column=0, padx=10)

btn_clear = tk.Button(btn_frame, text="🧹 Xóa",
                      command=clear,
                      bg="#ff8fa3",
                      fg="white",
                      font=("Segoe UI", 11, "bold"),
                      relief="flat",
                      padx=12)
btn_clear.grid(row=0, column=1)

btn_solve.bind("<Enter>", hover_green)
btn_solve.bind("<Leave>", leave_green)
btn_clear.bind("<Enter>", hover_pink)
btn_clear.bind("<Leave>", leave_pink)

# ===== OUTPUT =====
frame_out = tk.LabelFrame(left,
                          text="📊 Kết quả",
                          bg="white",
                          fg="#1d3557",
                          font=("Segoe UI", 11, "bold"),
                          padx=10, pady=10)
frame_out.pack(fill="both", expand=True)

output = tk.Text(frame_out,
                 font=("Segoe UI", 11),
                 bg="#f8fdfd",
                 fg="#333")
output.pack(fill="both", expand=True)

# STYLE TEXT
output.tag_config("title", font=("Segoe UI", 13, "bold"), foreground="#1d3557")
output.tag_config("highlight", foreground="#e63946", font=("Segoe UI", 11, "bold"))
output.tag_config("brain", foreground="#0d344d", font=("Segoe UI", 11, "bold"))

# ===== FORMULA =====
frame_formula = tk.LabelFrame(right,
                              text="📐 Công thức 🔺✨",
                              bg="white",
                              fg="#1d3557",
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