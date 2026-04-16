import tkinter as tk
from tkinter import ttk, messagebox
import math

class GiaoDienChinh:
    def __init__(self, window, controller=None):
        self.window = window
        self.controller = controller

        self.window.title("Triangle Expert System")
        self.window.geometry("1400x900")
        self.window.configure(bg="#0d1117")
        self.window.resizable(True, True)

        self.entries = {}
        self.anim_step = 0
        self.pulse_job = None

        # Color palette
        self.C = {
            "bg":        "#0d1117",
            "panel":     "#161b22",
            "panel2":    "#1c2128",
            "border":    "#30363d",
            "accent":    "#58a6ff",
            "accent2":   "#3fb950",
            "accent3":   "#f78166",
            "accent4":   "#d2a8ff",
            "text":      "#e6edf3",
            "muted":     "#8b949e",
            "hover":     "#21262d",
            "input_bg":  "#0d1117",
            "tag_side":  "#1f3a5f",
            "tag_angle": "#1f3d2a",
            "tag_other": "#3d2a1f",
        }

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        C = self.C

        style.configure("TFrame", background=C["bg"])

        style.configure("Solve.TButton",
            font=("Courier New", 10, "bold"),
            background=C["accent"], foreground="#0d1117", padding=12, relief="flat")
        style.map("Solve.TButton",
            background=[('active', '#79c0ff'), ('pressed', '#388bfd')])

        style.configure("Graph.TButton",
            font=("Courier New", 10, "bold"),
            background=C["accent2"], foreground="#0d1117", padding=12, relief="flat")
        style.map("Graph.TButton",
            background=[('active', '#56d364'), ('pressed', '#2ea043')])

        style.configure("Clear.TButton",
            font=("Courier New", 10, "bold"),
            background=C["accent3"], foreground="#0d1117", padding=12, relief="flat")
        style.map("Clear.TButton",
            background=[('active', '#ff9492'), ('pressed', '#da3633')])

        style.configure("Export.TButton",
            font=("Courier New", 10, "bold"),
            background=C["accent4"], foreground="#0d1117", padding=12, relief="flat")
        style.map("Export.TButton",
            background=[('active', '#e2c5ff'), ('pressed', '#a371f7')])

    def create_widgets(self):
        C = self.C

        # ── TOP HEADER BAR ──────────────────────────────────────────────
        header = tk.Frame(self.window, bg=C["panel"], height=56)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(header, text="▲  TRIANGLE EXPERT SYSTEM",
                 font=("Courier New", 14, "bold"),
                 bg=C["panel"], fg=C["accent"]).pack(side="left", padx=24, pady=14)

        self.status_label = tk.Label(header, text="● Sẵn sàng",
                 font=("Courier New", 10),
                 bg=C["panel"], fg=C["accent2"])
        self.status_label.pack(side="right", padx=24)

        tk.Label(header, text="Mạng ngữ nghĩa • Suy diễn tự động",
                 font=("Courier New", 9),
                 bg=C["panel"], fg=C["muted"]).pack(side="right", padx=10)

        # ── MAIN BODY ───────────────────────────────────────────────────
        body = tk.Frame(self.window, bg=C["bg"])
        body.pack(fill="both", expand=True, padx=12, pady=10)

        # ── LEFT PANEL: INPUT ───────────────────────────────────────────
        left = tk.Frame(body, bg=C["panel"], width=250)
        left.pack_propagate(False)
        left.pack(side="left", fill="y", padx=(0, 8))

        self._section_label(left, "// NHẬP DỮ LIỆU")

        # Triangle type quick-select
        type_frame = tk.Frame(left, bg=C["panel"])
        type_frame.pack(fill="x", padx=14, pady=(0, 10))
        tk.Label(type_frame, text="Loại tam giác nhanh:",
                 font=("Courier New", 8), bg=C["panel"], fg=C["muted"]).pack(anchor="w")
        btn_row = tk.Frame(type_frame, bg=C["panel"])
        btn_row.pack(fill="x", pady=4)
        for label, cmd in [("Vuông", self._preset_vuong),
                            ("Đều",  self._preset_deu),
                            ("Cân",  self._preset_can)]:
            b = tk.Button(btn_row, text=label,
                          font=("Courier New", 8, "bold"),
                          bg=C["border"], fg=C["text"],
                          relief="flat", padx=8, pady=4,
                          activebackground=C["hover"], activeforeground=C["accent"],
                          cursor="hand2", command=cmd)
            b.pack(side="left", padx=2)

        # Separator
        tk.Frame(left, bg=C["border"], height=1).pack(fill="x", padx=14, pady=6)

        vars_to_input = [
            ("Cạnh a", "a", C["tag_side"],  C["accent"]),
            ("Cạnh b", "b", C["tag_side"],  C["accent"]),
            ("Cạnh c", "c", C["tag_side"],  C["accent"]),
            ("Góc A°",  "A", C["tag_angle"], C["accent2"]),
            ("Góc B°",  "B", C["tag_angle"], C["accent2"]),
            ("Góc C°",  "C", C["tag_angle"], C["accent2"]),
        ]

        for label, var, bg_tag, fg_tag in vars_to_input:
            row = tk.Frame(left, bg=C["panel"])
            row.pack(fill="x", padx=14, pady=3)

            tag = tk.Label(row, text=label, font=("Courier New", 9, "bold"),
                           bg=bg_tag, fg=fg_tag,
                           width=8, anchor="w", padx=6, pady=3)
            tag.pack(side="left")

            ent = tk.Entry(row, font=("Courier New", 11),
                           bg=C["input_bg"], fg=C["text"],
                           relief="flat", borderwidth=0,
                           insertbackground=C["accent"],
                           selectbackground=C["accent"],
                           width=9)
            ent.pack(side="left", padx=(4, 0), ipady=4)
            ent.bind("<Return>", lambda e: self.handle_solve())
            ent.bind("<FocusIn>",  lambda e, w=ent: w.config(bg="#1a2332"))
            ent.bind("<FocusOut>", lambda e, w=ent: w.config(bg=C["input_bg"]))
            self.entries[var] = ent

        tk.Frame(left, bg=C["border"], height=1).pack(fill="x", padx=14, pady=10)

        # Buttons
        btn_pad = tk.Frame(left, bg=C["panel"])
        btn_pad.pack(fill="x", padx=14)
        ttk.Button(btn_pad, text="⚡  Giải ngay",    style="Solve.TButton",  command=self.handle_solve).pack(fill="x", pady=3)
        ttk.Button(btn_pad, text="◈  Xem đồ thị",   style="Graph.TButton",  command=self.handle_draw_graph).pack(fill="x", pady=3)
        ttk.Button(btn_pad, text="⟳  Làm mới",      style="Clear.TButton",  command=self.clear).pack(fill="x", pady=3)
        ttk.Button(btn_pad, text="↗  Xuất kết quả", style="Export.TButton", command=self.handle_export).pack(fill="x", pady=3)

        # ── MIDDLE PANEL: CANVAS + RESULTS ─────────────────────────────
        mid = tk.Frame(body, bg=C["bg"])
        mid.pack(side="left", fill="both", expand=True, padx=(0, 8))

        # Triangle canvas
        canvas_frame = tk.Frame(mid, bg=C["panel"], height=280)
        canvas_frame.pack(fill="x", pady=(0, 8))
        canvas_frame.pack_propagate(False)

        self._section_label(canvas_frame, "// HÌNH MINH HỌA TAM GIÁC")
        self.tri_canvas = tk.Canvas(canvas_frame, bg=C["panel"],
                                    highlightthickness=0, height=230)
        self.tri_canvas.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self._draw_placeholder_triangle()

        # Results
        res_frame = tk.Frame(mid, bg=C["panel"])
        res_frame.pack(fill="both", expand=True)

        header_row = tk.Frame(res_frame, bg=C["panel"])
        header_row.pack(fill="x")
        self._section_label(header_row, "// KẾT QUẢ & TIẾN TRÌNH SUY DIỄN")

        # Tabs
        self.tab_var = tk.StringVar(value="result")
        tab_bar = tk.Frame(res_frame, bg=C["panel"])
        tab_bar.pack(fill="x", padx=14)

        self.tab_btns = {}
        for tab_id, tab_name in [("result", "Kết quả"), ("trace", "Vết suy diễn"), ("summary", "Tóm tắt")]:
            b = tk.Button(tab_bar, text=tab_name,
                          font=("Courier New", 9, "bold"),
                          bg=C["accent"] if tab_id == "result" else C["border"],
                          fg="#0d1117" if tab_id == "result" else C["muted"],
                          relief="flat", padx=12, pady=5,
                          activebackground=C["hover"],
                          cursor="hand2",
                          command=lambda t=tab_id: self._switch_tab(t))
            b.pack(side="left", padx=2)
            self.tab_btns[tab_id] = b

        self.output = tk.Text(res_frame,
                              font=("Courier New", 10),
                              bg=C["input_bg"], fg=C["text"],
                              relief="flat", padx=16, pady=16,
                              insertbackground=C["accent"],
                              selectbackground=C["accent"],
                              spacing1=2, spacing3=4)
        self.output.pack(fill="both", expand=True, padx=10, pady=8)

        # Tags for colored output
        self.output.tag_configure("header",   font=("Courier New", 11, "bold"), foreground=C["accent"])
        self.output.tag_configure("subhead",  font=("Courier New", 10, "bold"), foreground=C["accent2"])
        self.output.tag_configure("value",    foreground=C["text"])
        self.output.tag_configure("formula",  foreground=C["muted"])
        self.output.tag_configure("warning",  foreground=C["accent3"])
        self.output.tag_configure("computed", foreground=C["accent4"])
        self.output.tag_configure("side_val", foreground=C["accent"])
        self.output.tag_configure("angle_val",foreground=C["accent2"])

        sb = tk.Scrollbar(res_frame, command=self.output.yview, bg=C["border"])
        self.output.config(yscrollcommand=sb.set)

        self._write_welcome()

        # ── RIGHT PANEL: KNOWLEDGE BASE ─────────────────────────────────
        right = tk.Frame(body, bg=C["panel"], width=260)
        right.pack_propagate(False)
        right.pack(side="right", fill="y")

        self._section_label(right, "// THƯ VIỆN TRI THỨC")

        self.kb_text = tk.Text(right,
                               font=("Courier New", 9),
                               bg=C["panel"], fg=C["muted"],
                               relief="flat", padx=14, pady=8,
                               spacing1=1, spacing3=3,
                               cursor="arrow")
        self.kb_text.pack(fill="both", expand=True, padx=4, pady=(0, 10))

        self.kb_text.tag_configure("group",  font=("Courier New", 9, "bold"), foreground=C["accent4"])
        self.kb_text.tag_configure("rule",   foreground=C["text"])
        self.kb_text.tag_configure("active", foreground=C["accent2"], font=("Courier New", 9, "bold"))

        self._populate_kb()

    # ── HELPERS ─────────────────────────────────────────────────────────

    def _section_label(self, parent, text):
        C = self.C
        f = tk.Frame(parent, bg=C["panel"])
        f.pack(fill="x", padx=14, pady=(12, 6))
        tk.Label(f, text=text, font=("Courier New", 10, "bold"),
                 bg=C["panel"], fg=C["accent"]).pack(side="left")
        tk.Frame(f, bg=C["border"], height=1).pack(side="left", fill="x", expand=True, padx=(8, 0), pady=7)

    def _populate_kb(self):
        groups = [
            ("LUẬT SUY DIỄN HÌNH HỌC", [
                "1. Kiểm tra BĐT tam giác",
                "2. Tam giác cân",
                "3. Tam giác đều",
                "4. Tam giác vuông",
                "5. Tam giác tù / nhọn",
                "6. Tam giác vuông cân",
            ]),
            ("GIẢI TAM GIÁC CƠ BẢN", [
                "7. Tổng ba góc = 180°",
                "8. Định lý Pytago",
                "9. Định lý Sin",
                "10. Định lý Cosin",
            ]),
            ("DIỆN TÍCH & CHU VI", [
                "11. Công thức Chu vi",
                "12. Công thức Heron",
                "13. S qua bán kính ngoại tiếp",
                "14. S qua bán kính nội tiếp",
                "15. S = ½ab·sin(C)",
            ]),
            ("ĐƯỜNG ĐẶC BIỆT", [
                "16. Đường cao",
                "17. Đường trung tuyến",
                "18. Đường phân giác",
                "19. Tỉ lệ đoạn phân giác",
            ]),
            ("TỌA ĐỘ", [
                "20. Tâm đường tròn ngoại tiếp",
                "21. Tâm đường tròn nội tiếp",
            ]),
        ]
        self.kb_rule_lines = {}  # map rule text -> line index
        line = 1
        for group_name, rules in groups:
            self.kb_text.insert(tk.END, f"\n▸ {group_name}\n", "group")
            line += 2
            for r in rules:
                self.kb_text.insert(tk.END, f"  {r}\n", "rule")
                self.kb_rule_lines[r] = line
                line += 1
        self.kb_text.config(state="disabled")

    def _write_welcome(self):
        C = self.C
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        msg = ()
        self.output.insert(tk.END, msg, "header")
        self.output.insert(tk.END, "  Hệ thống chuyên gia giải tam giác dựa trên mạng ngữ nghĩa.\n", "formula")
        self.output.insert(tk.END, "  Nhập ít nhất 3 dữ kiện (cạnh/góc) rồi nhấn ⚡ Giải ngay.\n\n", "formula")
        self.output.insert(tk.END, "  Phím tắt: [Enter] trong ô nhập = Giải ngay\n", "formula")
        self.output.config(state="disabled")

    def _draw_placeholder_triangle(self):
        self.tri_canvas.delete("all")
        C = self.C
        w, h = 400, 210
        # Draw faint grid
        for i in range(0, 500, 30):
            self.tri_canvas.create_line(i, 0, i, 250, fill=C["border"], width=1)
        for i in range(0, 260, 30):
            self.tri_canvas.create_line(0, i, 500, i, fill=C["border"], width=1)
        # Draw placeholder triangle
        pts = [200, 30, 80, 195, 320, 195]
        self.tri_canvas.create_polygon(pts, outline=C["border"], fill="", width=2, dash=(6, 4))
        self.tri_canvas.create_text(200, 18,  text="A", fill=C["muted"], font=("Courier New", 10, "bold"))
        self.tri_canvas.create_text(66,  205, text="B", fill=C["muted"], font=("Courier New", 10, "bold"))
        self.tri_canvas.create_text(334, 205, text="C", fill=C["muted"], font=("Courier New", 10, "bold"))
        self.tri_canvas.create_text(200, 120, text="Nhập dữ liệu để xem hình",
                                    fill=C["muted"], font=("Courier New", 9))

    def draw_triangle(self, a=None, b=None, c=None, A=None, B=None, C_angle=None,
                      S=None, R=None, r=None, tri_type=""):
        """Draw a scaled triangle on canvas with labels."""
        canvas = self.tri_canvas
        canvas.delete("all")
        C = self.C

        cw = canvas.winfo_width()  or 400
        ch = canvas.winfo_height() or 210

        # Draw grid
        for i in range(0, cw + 30, 30):
            canvas.create_line(i, 0, i, ch, fill=C["border"], width=1)
        for i in range(0, ch + 30, 30):
            canvas.create_line(0, i, cw, i, fill=C["border"], width=1)

        # Try to reconstruct triangle coordinates from sides a, b, c
        if a and b and c:
            # Place B at origin, C at (a, 0), find A
            bx, by = 0.0, 0.0
            cx, cy = float(a), 0.0
            # cos(B) from law of cosines: b²=a²+c²-2ac·cosB → cosB=(a²+c²-b²)/(2ac)
            cos_B = (a**2 + c**2 - b**2) / (2 * a * c)
            cos_B = max(-1, min(1, cos_B))
            sin_B = math.sqrt(1 - cos_B**2)
            ax = c * cos_B
            ay = -c * sin_B  # negative = upward in canvas

            # Scale & center
            all_x = [bx, cx, ax]
            all_y = [by, cy, ay]
            min_x, max_x = min(all_x), max(all_x)
            min_y, max_y = min(all_y), max(all_y)
            span_x = max_x - min_x or 1
            span_y = max_y - min_y or 1

            margin = 48
            scale = min((cw - 2*margin) / span_x, (ch - 2*margin) / span_y)

            def tx(x): return margin + (x - min_x) * scale
            def ty(y): return ch - margin - (y - min_y) * scale  # flip y

            px = [tx(bx), tx(cx), tx(ax)]
            py = [ty(by), ty(cy), ty(ay)]

            # Glow effect (shadow)
                        # Vẽ tam giác với glow effect (phiên bản tương thích Tkinter)
            pts_flat = [px[0], py[0], px[1], py[1], px[2], py[2]]
            
            # Glow ngoài
            canvas.create_polygon(pts_flat, 
                                  outline="#58a6ff", 
                                  fill="", 
                                  width=9)

            canvas.create_polygon(pts_flat, 
                                  outline="#58a6ff", 
                                  fill="", 
                                  width=6)
            
            # Thân tam giác
            canvas.create_polygon(pts_flat, 
                                  outline=C["accent"], 
                                  fill="#58a6ff", 
                                  width=3)

            # Circumscribed circle
            if R:
                r_px = R * scale
                ox = sum(px) / 3; oy = sum(py) / 3
                # better: compute real circumcenter
                canvas.create_oval(ox - r_px, oy - r_px,
                                   ox + r_px, oy + r_px,
                                   outline="#f78166", width=1, dash=(4,4))

            # Inscribed circle
            if r:
                r_px = r * scale
                # incenter
                perimeter = a + b + c
                ix_c = (a*ax + b*bx + c*cx) / perimeter
                iy_c = (a*ay + b*by + c*cy) / perimeter
                canvas.create_oval(tx(ix_c) - r_px, ty(iy_c) - r_px,
                                   tx(ix_c) + r_px, ty(iy_c) + r_px,
                                   outline="#3fb950", width=1, dash=(3,3))

            # Vertex labels with values
            offsets = [(-16, 10), (10, 10), (0, -18)]
            names = ["B", "C", "A"]
            angles = [B, C_angle, A]
            for i, (name, ang) in enumerate(zip(names, angles)):
                ox, oy = offsets[i]
                lbl = f"{name}"
                if ang: lbl += f"\n{ang:.1f}°"
                canvas.create_text(px[i] + ox, py[i] + oy,
                                   text=lbl, fill=C["accent2"],
                                   font=("Courier New", 9, "bold"), justify="center")

            # Side labels
            mids = [(0, 1, "a", a), (1, 2, "c", c), (0, 2, "b", b)]
            for i1, i2, name, val in mids:
                mx = (px[i1] + px[i2]) / 2
                my = (py[i1] + py[i2]) / 2
                canvas.create_text(mx, my, text=f"{name}={val:.2f}",
                                   fill=C["accent"],
                                   font=("Courier New", 8, "bold"))

            # Type badge
            if tri_type:
                canvas.create_rectangle(6, 6, 6 + len(tri_type)*8 + 10, 22,
                                        fill=C["panel2"], outline=C["border"])
                canvas.create_text(11 + len(tri_type)*4, 14,
                                   text=tri_type, fill=C["accent4"],
                                   font=("Courier New", 8, "bold"))
        else:
            self._draw_placeholder_triangle()

    # ── TAB SWITCHING ────────────────────────────────────────────────────

    def _switch_tab(self, tab_id):
        C = self.C
        self.tab_var.set(tab_id)
        for tid, btn in self.tab_btns.items():
            if tid == tab_id:
                btn.config(bg=C["accent"], fg="#0d1117")
            else:
                btn.config(bg=C["border"], fg=C["muted"])

        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        if tab_id == "result":
            self.output.insert(tk.END, self._last_result or "Chưa có kết quả.", "value")
        elif tab_id == "trace":
            self.output.insert(tk.END, self._last_trace  or "Chưa có vết suy diễn.", "formula")
        elif tab_id == "summary":
            self.output.insert(tk.END, self._last_summary or "Chưa có tóm tắt.", "value")
        self.output.config(state="disabled")

    # ── PRESET BUTTONS ───────────────────────────────────────────────────

    def _preset_vuong(self):
        self.clear()
        self.entries["a"].insert(0, "5")
        self.entries["b"].insert(0, "3")
        self.entries["c"].insert(0, "4")

    def _preset_deu(self):
        self.clear()
        self.entries["a"].insert(0, "6")
        self.entries["b"].insert(0, "6")
        self.entries["c"].insert(0, "6")

    def _preset_can(self):
        self.clear()
        self.entries["a"].insert(0, "8")
        self.entries["b"].insert(0, "5")
        self.entries["c"].insert(0, "5")

    # ── STATUS ───────────────────────────────────────────────────────────

    def _set_status(self, text, color=None):
        self.status_label.config(text=text,
                                 fg=color or self.C["accent2"])

    # ── MAIN SOLVE ───────────────────────────────────────────────────────

    def handle_solve(self):
        inputs = {k: e.get().strip() for k, e in self.entries.items() if e.get().strip()}
        if not inputs:
            messagebox.showwarning("Thông báo", "Vui lòng nhập ít nhất một vài dữ kiện!")
            return

        self._set_status("● Đang giải...", self.C["accent"])
        self.window.update_idletasks()

        if self.controller:
            try:
                self.controller.reset()
                self.controller.nhap_du_lieu_ban_dau(inputs)
                self.controller.thuc_thi_suy_dien()

                ket_qua   = self.controller.lay_ket_qua_dinh_dang()
                vet_suy   = self.controller.lay_vet_suy_dien_dinh_dang()
                summary   = self.controller.lay_tom_tat()
                tri_data  = self.controller.lay_du_lieu_tam_giac()
                tri_type  = self.controller.lay_loai_tam_giac()

                self._last_result  = ket_qua
                self._last_trace   = vet_suy
                self._last_summary = summary

                self.hien_thi_ket_qua(ket_qua, vet_suy)
                self.draw_triangle(**tri_data, tri_type=tri_type)
                self._highlight_active_rules(vet_suy)
                self._set_status("● Giải xong", self.C["accent2"])

            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
                self._set_status("● Lỗi", self.C["accent3"])
        else:
            messagebox.showwarning("Thông báo", "Chưa kết nối controller!")

    def hien_thi_ket_qua(self, ket_qua, vet_suy_dien):
        C = self.C
        self._switch_tab("result")
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)

        # ── GIÁ TRỊ TÌM ĐƯỢC ──
        self.output.insert(tk.END, "╔══ GIÁ TRỊ TÌM ĐƯỢC ══════════════════════════════╗\n", "header")
        lines = ket_qua.strip().split("\n")
        for line in lines:
            if "=" in line:
                parts = line.split("=", 1)
                key = parts[0].strip()
                if key in ["a", "b", "c"]:
                    tag = "side_val"
                elif key in ["A", "B", "C"]:
                    tag = "angle_val"
                else:
                    tag = "computed"
                self.output.insert(tk.END, f"  {line}\n", tag)
            else:
                self.output.insert(tk.END, f"  {line}\n", "formula")
        self.output.insert(tk.END, "╚════════════════════════════════════════════════════╝\n\n", "header")

        # ── VẾT SUY DIỄN ──
        self.output.insert(tk.END, "╔══ CÁC BƯỚC GIẢI CHI TIẾT ════════════════════════╗\n", "subhead")
        steps = vet_suy_dien.strip().split("\n")
        for i, step in enumerate(steps, 1):
            self.output.insert(tk.END, f"  [{i:02d}] {step}\n", "formula")
        self.output.insert(tk.END, "╚════════════════════════════════════════════════════╝\n", "subhead")

        self.output.config(state="disabled")

    def _highlight_active_rules(self, vet_suy):
        """Highlight rules used in the KB panel"""
        self.kb_text.config(state="normal")
        rule_keywords = {
            "Pytago": "8. Định lý Pytago",
            "Sin": "9. Định lý Sin",
            "Cosin": "10. Định lý Cosin",
            "Heron": "12. Công thức Heron",
            "Chu vi": "11. Công thức Chu vi",
            "đường cao": "16. Đường cao",
            "Trung Tuyến": "17. Đường trung tuyến",
            "phân giác": "18. Đường phân giác",
            "ngoại tiếp": "13. S qua bán kính ngoại tiếp",
            "nội tiếp": "14. S qua bán kính nội tiếp",
            "sinC": "15. S = ½ab·sin(C)",
            "Tổng 3 góc": "7. Tổng ba góc = 180°",
        }
        # Reset all to "rule"
        self.kb_text.tag_remove("active", "1.0", tk.END)
        for keyword, rule_text in rule_keywords.items():
            if keyword.lower() in vet_suy.lower():
                # Find and highlight
                start = "1.0"
                while True:
                    pos = self.kb_text.search(rule_text, start, tk.END)
                    if not pos:
                        break
                    end = f"{pos}+{len(rule_text)}c"
                    self.kb_text.tag_add("active", pos, end)
                    start = end
        self.kb_text.config(state="disabled")

    def clear(self):
        for ent in self.entries.values():
            ent.delete(0, tk.END)
        self._last_result = self._last_trace = self._last_summary = None
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.config(state="disabled")
        self._draw_placeholder_triangle()
        self._set_status("● Sẵn sàng", self.C["accent2"])
        # Reset KB highlights
        self.kb_text.config(state="normal")
        self.kb_text.tag_remove("active", "1.0", tk.END)
        self.kb_text.config(state="disabled")
        if self.controller:
            self.controller.reset()

    def handle_draw_graph(self):
        if self.controller:
            self.controller.ve_do_thi()
        else:
            messagebox.showwarning("Thông báo", "Chưa kết nối được với bộ xử lý đồ thị!")

    def handle_export(self):
        """Export results to a text file"""
        if not hasattr(self, '_last_result') or not self._last_result:
            messagebox.showwarning("Thông báo", "Chưa có kết quả để xuất!")
            return
        try:
            from tkinter import filedialog
            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Xuất kết quả"
            )
            if filepath:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("=== TRIANGLE EXPERT SYSTEM - KẾT QUẢ ===\n\n")
                    f.write("--- GIÁ TRỊ TÌM ĐƯỢC ---\n")
                    f.write(self._last_result + "\n\n")
                    f.write("--- VẾT SUY DIỄN ---\n")
                    f.write(self._last_trace + "\n")
                messagebox.showinfo("Thành công", f"Đã xuất kết quả ra:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")