import tkinter as tk
from tkinter import ttk, messagebox

from database import create_database
from student import (
    add_student,
    get_all_students,
    find_student,
    update_student,
    delete_student
)
from grades import (
    add_grade,
    get_student_grades,
    calculate_average,
    get_top_students,
    sort_students_by_average
)


# ==============================
# ТҮСТЕР ЖӘНЕ ДИЗАЙН
# ==============================

BG = "#F1F5F9"
WHITE = "#FFFFFF"
DARK = "#172554"
BLUE = "#DBEAFE"
TEXT = "#1E293B"
GRAY = "#64748B"
GREEN = "#DCFCE7"
RED = "#FEE2E2"
YELLOW = "#FEF3C7"


class StudentManagementApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1150x750")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG)

        create_database()

        self.setup_styles()
        self.create_interface()
        self.show_students()

    # ==============================
    # СТИЛЬДЕР
    # ==============================

    def setup_styles(self):

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            font=("Arial", 11),
            rowheight=34,
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 11, "bold"),
            background=BLUE,
            foreground=DARK,
            padding=10
        )

        style.map(
            "Treeview",
            background=[("selected", "#BFDBFE")],
            foreground=[("selected", DARK)]
        )

        style.configure(
            "Modern.TButton",
            font=("Arial", 11, "bold"),
            foreground=DARK,
            background=BLUE,
            padding=(18, 12),
            borderwidth=1,
            relief="flat"
        )

        style.map(
            "Modern.TButton",
            foreground=[
                ("active", DARK),
                ("disabled", GRAY)
            ],
            background=[
                ("active", "#BFDBFE"),
                ("pressed", "#93C5FD")
            ]
        )

        style.configure(
            "Success.TButton",
            font=("Arial", 11, "bold"),
            foreground="#14532D",
            background=GREEN,
            padding=(18, 12)
        )

        style.configure(
            "Danger.TButton",
            font=("Arial", 11, "bold"),
            foreground="#991B1B",
            background=RED,
            padding=(18, 12)
        )

        style.configure(
            "Warning.TButton",
            font=("Arial", 11, "bold"),
            foreground="#92400E",
            background=YELLOW,
            padding=(18, 12)
        )

    # ==============================
    # НЕГІЗГІ ИНТЕРФЕЙС
    # ==============================

    def create_interface(self):

        header = tk.Frame(
            self.root,
            bg=DARK,
            height=100
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="STUDENT MANAGEMENT SYSTEM",
            font=("Arial", 23, "bold"),
            bg=DARK,
            fg=WHITE
        ).pack(pady=(18, 4))

        tk.Label(
            header,
            text="Студенттердің ақпаратын басқару жүйесі",
            font=("Arial", 12),
            bg=DARK,
            fg="#CBD5E1"
        ).pack()

        navigation = tk.Frame(
            self.root,
            bg=WHITE,
            padx=15,
            pady=15
        )

        navigation.pack(
            fill="x",
            padx=20,
            pady=15
        )

        buttons = [
            ("Студенттер", self.show_students),
            ("Студент қосу", self.show_add_student),
            ("Бағалар", self.show_grades),
            ("Үлгерім", self.show_performance)
        ]

        for text, command in buttons:

            ttk.Button(
                navigation,
                text=text,
                command=command,
                style="Modern.TButton"
            ).pack(
                side="left",
                padx=6
            )

        self.content = tk.Frame(
            self.root,
            bg=BG
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def title(self, text):

        tk.Label(
            self.content,
            text=text,
            font=("Arial", 21, "bold"),
            bg=BG,
            fg=DARK
        ).pack(
            anchor="w",
            pady=(5, 20)
        )

    # ==============================
    # КЕСТЕ ЖАСАУ
    # ==============================

    def create_table(self, parent, columns, headings):

        frame = tk.Frame(
            parent,
            bg=WHITE,
            padx=5,
            pady=5
        )

        frame.pack(
            fill="both",
            expand=True
        )

        tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        for column, heading in zip(columns, headings):

            tree.heading(
                column,
                text=heading
            )

            tree.column(
                column,
                width=150,
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=tree.yview
        )

        tree.configure(
            yscrollcommand=scrollbar.set
        )

        tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        return tree

    # ==============================
    # СТУДЕНТТЕР ТІЗІМІ
    # ==============================

    def show_students(self):

        self.clear_content()
        self.title("Студенттер тізімі")

        search_frame = tk.Frame(
            self.content,
            bg=BG
        )

        search_frame.pack(
            fill="x",
            pady=10
        )

        tk.Label(
            search_frame,
            text="Студент ID:",
            bg=BG,
            fg=TEXT,
            font=("Arial", 11, "bold")
        ).pack(side="left")

        search_entry = ttk.Entry(
            search_frame,
            font=("Arial", 12),
            width=18
        )

        search_entry.pack(
            side="left",
            padx=12
        )

        def search():

            value = search_entry.get().strip()

            if not value:
                self.show_students()
                return

            try:

                student_id = int(value)
                student = find_student(student_id)

                for item in self.student_table.get_children():
                    self.student_table.delete(item)

                if student:

                    self.student_table.insert(
                        "",
                        "end",
                        values=student
                    )

                else:

                    messagebox.showinfo(
                        "Іздеу нәтижесі",
                        "Студент табылмады!"
                    )

            except ValueError:

                messagebox.showerror(
                    "Қате",
                    "ID сан болуы керек!"
                )

        ttk.Button(
            search_frame,
            text="Іздеу",
            command=search,
            style="Modern.TButton"
        ).pack(side="left")

        ttk.Button(
            search_frame,
            text="Барлығын көрсету",
            command=self.show_students,
            style="Modern.TButton"
        ).pack(
            side="left",
            padx=10
        )

        self.student_table = self.create_table(
            self.content,
            ("id", "name", "group", "age", "phone"),
            ("ID", "Аты-жөні", "Тобы", "Жасы", "Телефон")
        )

        for student in get_all_students():

            self.student_table.insert(
                "",
                "end",
                values=student
            )

        actions = tk.Frame(
            self.content,
            bg=BG
        )

        actions.pack(
            fill="x",
            pady=15
        )

        ttk.Button(
            actions,
            text="Өзгерту",
            command=self.edit_selected_student,
            style="Warning.TButton"
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            actions,
            text="Жою",
            command=self.remove_selected_student,
            style="Danger.TButton"
        ).pack(
            side="left",
            padx=5
        )

    # ==============================
    # СТУДЕНТ ҚОСУ
    # ==============================

    def show_add_student(self):

        self.clear_content()
        self.title("Жаңа студентті тіркеу")

        form = tk.Frame(
            self.content,
            bg=WHITE,
            padx=35,
            pady=30
        )

        form.pack(fill="x")

        fields = [
            ("Аты-жөні", "name"),
            ("Тобы", "group"),
            ("Жасы", "age"),
            ("Телефон", "phone")
        ]

        entries = {}

        for row, (label, key) in enumerate(fields):

            tk.Label(
                form,
                text=label,
                bg=WHITE,
                fg=TEXT,
                font=("Arial", 11, "bold")
            ).grid(
                row=row,
                column=0,
                sticky="w",
                pady=12
            )

            entry = ttk.Entry(
                form,
                width=42,
                font=("Arial", 12)
            )

            entry.grid(
                row=row,
                column=1,
                padx=20,
                pady=12
            )

            entries[key] = entry

        def save():

            try:

                name = entries["name"].get().strip()
                group = entries["group"].get().strip()
                age_text = entries["age"].get().strip()
                phone = entries["phone"].get().strip()

                age = int(age_text) if age_text else None

                student_id = add_student(
                    name,
                    group,
                    age,
                    phone
                )

                messagebox.showinfo(
                    "Сәтті",
                    f"Студент тіркелді!\nID: {student_id}"
                )

                self.show_students()

            except ValueError as error:

                messagebox.showerror(
                    "Қате",
                    str(error)
                )

        ttk.Button(
            form,
            text="Студентті сақтау",
            command=save,
            style="Success.TButton"
        ).grid(
            row=5,
            column=1,
            pady=25
        )

    # ==============================
    # СТУДЕНТТІ ӨЗГЕРТУ
    # ==============================

    def edit_selected_student(self):

        selected = self.student_table.selection()

        if not selected:

            messagebox.showwarning(
                "Ескерту",
                "Алдымен студентті таңдаңыз!"
            )

            return

        values = self.student_table.item(
            selected[0],
            "values"
        )

        student_id = int(values[0])

        window = tk.Toplevel(self.root)

        window.title("Студентті өзгерту")
        window.geometry("500x400")
        window.configure(bg=WHITE)

        fields = [
            ("Аты-жөні", values[1]),
            ("Тобы", values[2]),
            ("Жасы", values[3]),
            ("Телефон", values[4])
        ]

        entries = []

        for i, (label, value) in enumerate(fields):

            tk.Label(
                window,
                text=label,
                bg=WHITE,
                fg=TEXT,
                font=("Arial", 11)
            ).grid(
                row=i,
                column=0,
                padx=20,
                pady=15
            )

            entry = ttk.Entry(
                window,
                width=32
            )

            entry.insert(0, value)

            entry.grid(
                row=i,
                column=1,
                padx=10
            )

            entries.append(entry)

        def save_changes():

            try:

                name = entries[0].get().strip()
                group = entries[1].get().strip()
                age_text = entries[2].get().strip()
                phone = entries[3].get().strip()

                age = int(age_text) if age_text else None

                update_student(
                    student_id,
                    name,
                    group,
                    age,
                    phone
                )

                messagebox.showinfo(
                    "Сәтті",
                    "Мәліметтер өзгертілді!"
                )

                window.destroy()
                self.show_students()

            except ValueError as error:

                messagebox.showerror(
                    "Қате",
                    str(error)
                )

        ttk.Button(
            window,
            text="Өзгерістерді сақтау",
            command=save_changes,
            style="Success.TButton"
        ).grid(
            row=5,
            column=1,
            pady=25
        )

    # ==============================
    # СТУДЕНТТІ ЖОЮ
    # ==============================

    def remove_selected_student(self):

        selected = self.student_table.selection()

        if not selected:

            messagebox.showwarning(
                "Ескерту",
                "Студентті таңдаңыз!"
            )

            return

        values = self.student_table.item(
            selected[0],
            "values"
        )

        student_id = int(values[0])

        confirm = messagebox.askyesno(
            "Растау",
            "Студентті жойғыңыз келе ме?"
        )

        if confirm:

            delete_student(student_id)

            self.show_students()

    # ==============================
    # БАҒАЛАР
    # ==============================

    def show_grades(self):

        self.clear_content()
        self.title("Студенттердің бағалары")

        form = tk.Frame(
            self.content,
            bg=WHITE,
            padx=25,
            pady=20
        )

        form.pack(
            fill="x",
            pady=10
        )

        labels = [
            "Студент ID",
            "Пән атауы",
            "Баға (0–100)"
        ]

        entries = []

        for i, label in enumerate(labels):

            tk.Label(
                form,
                text=label,
                bg=WHITE,
                fg=TEXT,
                font=("Arial", 11, "bold")
            ).grid(
                row=i,
                column=0,
                padx=10,
                pady=12
            )

            entry = ttk.Entry(
                form,
                width=40
            )

            entry.grid(
                row=i,
                column=1,
                padx=15
            )

            entries.append(entry)

        result = tk.Label(
            form,
            text="",
            bg=WHITE,
            fg=DARK,
            font=("Arial", 12, "bold")
        )

        result.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=15
        )

        def show_student_grades():

            try:

                student_id = int(entries[0].get())

                student = find_student(student_id)

                if student is None:

                    messagebox.showwarning(
                        "Ескерту",
                        "Студент табылмады!"
                    )

                    return

                grades = get_student_grades(student_id)

                for item in grade_table.get_children():
                    grade_table.delete(item)

                for grade in grades:

                    grade_table.insert(
                        "",
                        "end",
                        values=grade
                    )

                average = calculate_average(student_id)

                if average is None:
                    result.config(text="Бағалар енгізілмеген")
                else:
                    result.config(text=f"Орташа бал: {average}")

            except ValueError:

                messagebox.showerror(
                    "Қате",
                    "Студент ID дұрыс енгізілмеген!"
                )

        def save_grade():

            try:

                student_id = int(entries[0].get())
                subject = entries[1].get().strip()
                grade = float(entries[2].get())

                add_grade(
                    student_id,
                    subject,
                    grade
                )

                messagebox.showinfo(
                    "Сәтті",
                    "Баға сақталды!"
                )

                show_student_grades()

            except ValueError as error:

                messagebox.showerror(
                    "Қате",
                    str(error)
                )

        ttk.Button(
            form,
            text="Бағаны сақтау",
            command=save_grade,
            style="Success.TButton"
        ).grid(
            row=3,
            column=1,
            pady=10
        )

        ttk.Button(
            form,
            text="Бағаларды көрсету",
            command=show_student_grades,
            style="Modern.TButton"
        ).grid(
            row=4,
            column=1,
            pady=5
        )

        grade_table = self.create_table(
            self.content,
            ("id", "subject", "grade"),
            ("ID", "Пән", "Баға")
        )

    # ==============================
    # ҮЛГЕРІМ
    # ==============================

    def show_performance(self):

        self.clear_content()
        self.title("Студенттердің оқу үлгерімі")

        controls = tk.Frame(
            self.content,
            bg=BG
        )

        controls.pack(
            fill="x",
            pady=10
        )

        performance_table = self.create_table(
            self.content,
            ("id", "name", "group", "average"),
            ("ID", "Аты-жөні", "Тобы", "Орташа бал")
        )

        def show_all():

            for item in performance_table.get_children():
                performance_table.delete(item)

            for student in sort_students_by_average():

                performance_table.insert(
                    "",
                    "end",
                    values=student
                )

        def show_top():

            for item in performance_table.get_children():
                performance_table.delete(item)

            for student in get_top_students():

                performance_table.insert(
                    "",
                    "end",
                    values=student
                )

        ttk.Button(
            controls,
            text="Барлық студенттер",
            command=show_all,
            style="Modern.TButton"
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            controls,
            text="Үздік студенттер (85+)",
            command=show_top,
            style="Success.TButton"
        ).pack(
            side="left",
            padx=5
        )

        show_all()


# ==============================
# БАҒДАРЛАМАНЫ ІСКЕ ҚОСУ
# ==============================

if __name__ == "__main__":

    root = tk.Tk()

    app = StudentManagementApp(root)

    root.mainloop()