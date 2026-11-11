import tkinter as tk
from tkinter import messagebox

from Backend import (lettered_grade_list, MarkToScale, ScaleToGpa,
                     calculateAvgMark, calculateAvgGPA)

BG, CARD, CARD2 = "#0b1020", "#151b30", "#1e2640"
FG, MUTED, ACCENT, ACCENT2 = "#e8ecf8", "#8c97b8", "#7c5cff", "#5b8cff"
GOOD, WARN, BAD = "#2ee6a6", "#ffc857", "#ff5c7a"
FONT = "Segoe UI"


def grade_color(gp):
    return GOOD if gp >= 3.0 else WARN if gp >= 2.0 else BAD


class HoverButton(tk.Button):
    def __init__(self, master, bg, hover, **kw):
        super().__init__(master, bg=bg, activebackground=hover, fg="white",
                         activeforeground="white", relief="flat", bd=0,
                         cursor="hand2", font=(FONT, 10, "bold"), **kw)
        self.bind("<Enter>", lambda e: self.config(bg=hover))
        self.bind("<Leave>", lambda e: self.config(bg=bg))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GPA Calculator")
        self.geometry("1020x640")
        self.minsize(900, 560)
        self.configure(bg=BG)
        self.rows = []
        self._header()
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(0, weight=1)
        self._input_panel(body)
        self._result_panel(body)
        for i in range(4):
            self.add_row()

    # ───── layout ─────
    def _header(self):
        h = tk.Frame(self, bg=BG)
        h.pack(fill="x", padx=24, pady=(20, 14))
        tk.Label(h, text="🎓  GPA Calculator", bg=BG, fg=FG,
                 font=(FONT, 22, "bold")).pack(side="left")
        tk.Label(h, text="enter your courses, get your grade instantly",
                 bg=BG, fg=MUTED, font=(FONT, 10)).pack(side="left", padx=14, pady=(10, 0))

    def _input_panel(self, parent):
        card = tk.Frame(parent, bg=CARD, padx=18, pady=16)
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        card.rowconfigure(1, weight=1)
        card.columnconfigure(0, weight=1)

        head = tk.Frame(card, bg=CARD)
        head.grid(row=0, column=0, sticky="ew")
        for text, w in (("Course", 22), ("Credits", 8), ("Mark /100", 10), ("Grade", 7)):
            tk.Label(head, text=text.upper(), bg=CARD, fg=MUTED, width=w,
                     anchor="w", font=(FONT, 8, "bold")).pack(side="left", padx=4)

        wrap = tk.Frame(card, bg=CARD)
        wrap.grid(row=1, column=0, sticky="nsew", pady=8)
        self.canvas = tk.Canvas(wrap, bg=CARD, highlightthickness=0)
        sb = tk.Scrollbar(wrap, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.rows_frame = tk.Frame(self.canvas, bg=CARD)
        self.canvas.create_window((0, 0), window=self.rows_frame, anchor="nw")
        self.rows_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(
            -1 * (e.delta // 120), "units"))

        btns = tk.Frame(card, bg=CARD)
        btns.grid(row=2, column=0, sticky="ew")
        HoverButton(btns, CARD2, "#2a3358", text="＋  Add course", padx=14, pady=8,
                    command=self.add_row).pack(side="left")
        HoverButton(btns, CARD2, "#2a3358", text="Clear", padx=14, pady=8,
                    command=self.clear).pack(side="left", padx=8)
        HoverButton(btns, ACCENT, "#926dff", text="Calculate  →", padx=22, pady=8,
                    command=self.calculate).pack(side="right")

    def _result_panel(self, parent):
        card = tk.Frame(parent, bg=CARD, padx=18, pady=16)
        card.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        tk.Label(card, text="YOUR GPA", bg=CARD, fg=MUTED,
                 font=(FONT, 9, "bold")).pack(anchor="w")
        self.gpa_lbl = tk.Label(card, text="—", bg=CARD, fg=ACCENT2,
                                font=(FONT, 54, "bold"))
        self.gpa_lbl.pack(anchor="w")

        stats = tk.Frame(card, bg=CARD)
        stats.pack(fill="x", pady=(0, 10))
        self.avg_lbl = self._stat(stats, "AVERAGE MARK")
        self.cred_lbl = self._stat(stats, "TOTAL CREDITS")

        tk.Label(card, text="BREAKDOWN", bg=CARD, fg=MUTED,
                 font=(FONT, 9, "bold")).pack(anchor="w", pady=(6, 4))
        self.bars = tk.Canvas(card, bg=CARD, highlightthickness=0)
        self.bars.pack(fill="both", expand=True)

    def _stat(self, parent, title):
        f = tk.Frame(parent, bg=CARD2, padx=14, pady=10)
        f.pack(side="left", fill="x", expand=True, padx=(0, 8))
        tk.Label(f, text=title, bg=CARD2, fg=MUTED, font=(FONT, 8, "bold")).pack(anchor="w")
        v = tk.Label(f, text="—", bg=CARD2, fg=FG, font=(FONT, 16, "bold"))
        v.pack(anchor="w")
        return v

    # ───── rows ─────
    def _entry(self, parent, var, width):
        e = tk.Entry(parent, textvariable=var, width=width, bg=CARD2, fg=FG,
                     insertbackground=FG, relief="flat", font=(FONT, 11),
                     highlightthickness=2, highlightbackground=CARD2,
                     highlightcolor=ACCENT)
        return e

    def add_row(self, name="", credit="3", mark=""):
        f = tk.Frame(self.rows_frame, bg=CARD)
        f.pack(fill="x", pady=4)
        vn, vc, vm = tk.StringVar(value=name), tk.StringVar(value=credit), tk.StringVar(value=mark)
        self._entry(f, vn, 22).pack(side="left", padx=4, ipady=5)
        self._entry(f, vc, 8).pack(side="left", padx=4, ipady=5)
        self._entry(f, vm, 10).pack(side="left", padx=4, ipady=5)
        grade = tk.Label(f, text="–", bg=CARD, fg=MUTED, width=5, font=(FONT, 12, "bold"))
        grade.pack(side="left", padx=4)
        row = dict(frame=f, name=vn, credit=vc, mark=vm, grade=grade)
        tk.Button(f, text="✕", bg=CARD, fg=MUTED, activebackground=CARD,
                  activeforeground=BAD, relief="flat", bd=0, cursor="hand2",
                  command=lambda r=row: self.remove_row(r)).pack(side="left", padx=4)
        self.rows.append(row)

    def remove_row(self, row):
        row["frame"].destroy()
        self.rows.remove(row)

    def clear(self):
        for r in self.rows[:]:
            self.remove_row(r)
        for _ in range(4):
            self.add_row()
        self.gpa_lbl.config(text="—", fg=ACCENT2)
        self.avg_lbl.config(text="—")
        self.cred_lbl.config(text="—")
        self.bars.delete("all")

    # ───── logic ─────
    def calculate(self):
        courses, marks, credits, used = [], [], [], []
        for i, r in enumerate(self.rows, 1):
            if not r["mark"].get().strip() and not r["name"].get().strip():
                continue  # ignore empty rows
            try:
                m, c = float(r["mark"].get()), float(r["credit"].get())
                assert 0 <= m <= 100 and c > 0
            except (ValueError, AssertionError):
                messagebox.showerror("Invalid input",
                                     f"Row {i}: mark must be 0–100 and credits must be > 0.")
                return
            courses.append(r["name"].get().strip() or f"Course {i}")
            marks.append(m)
            credits.append(c)
            used.append(r)
        if not marks:
            messagebox.showinfo("Nothing to calculate", "Add at least one course with a mark.")
            return

        letters = []
        MarkToScale(marks, letters)
        points = ScaleToGpa(lettered_grade_list, letters, [])
        for r, l in zip(used, letters):
            r["grade"].config(text=l.strip())
        gpa = calculateAvgGPA(points, credits)
        self.gpa_lbl.config(text=f"{gpa:.2f}", fg=grade_color(gpa))
        self.avg_lbl.config(text=f"{calculateAvgMark(marks):.1f}")
        self.cred_lbl.config(text=f"{sum(credits):g}")
        self._draw_bars(courses, marks, letters, points)

    def _draw_bars(self, courses, marks, letters, points):
        c = self.bars
        c.delete("all")
        c.update_idletasks()
        w = max(c.winfo_width(), 260)
        for i, (n, m, l, p) in enumerate(zip(courses, marks, letters, points)):
            y = i * 44 + 4
            c.create_text(0, y, text=n[:26], anchor="nw", fill=FG, font=(FONT, 9))
            c.create_text(w, y, text=f"{l.strip()}  ·  {m:g}", anchor="ne",
                          fill=grade_color(p), font=(FONT, 9, "bold"))
            c.create_rectangle(0, y + 20, w, y + 28, fill=CARD2, outline="")
            c.create_rectangle(0, y + 20, w * m / 100, y + 28,
                               fill=grade_color(p), outline="")


if __name__ == "__main__":
    App().mainloop()