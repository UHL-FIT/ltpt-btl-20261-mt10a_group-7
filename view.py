import tkinter as tk
from tkinter import ttk

class StudentView:
    def __init__(self, root, controller=None):
        self.root = root
        self.controller = controller
        
        self.root.title("Quản lý Học bổng 2026 (MVC)")
        self.root.geometry("1050x650") 
        self.root.configure(bg="#0d1622")
        
        title_label = tk.Label(self.root, text="QUẢN LÝ XÉT DUYỆT HỌC BỔNG", 
                               font=("Arial", 16, "bold"), fg="#38bdf8", bg="#0d1622")
        title_label.pack(pady=15)
        
        btn_frame = tk.Frame(self.root, bg="#0d1622")
        btn_frame.pack(pady=10)
        
        btn_config = {"font": ("Arial", 10, "bold"), "fg": "white", "bg": "#112240", "bd": 1, "relief": "solid", "padx": 10, "pady": 5, "cursor": "hand2"}
        
        self.btn_add = tk.Button(btn_frame, text="THÊM SINH VIÊN", highlightbackground="#10b981", **btn_config)
        self.btn_add.config(highlightthickness=1, fg="#10b981")
        self.btn_add.pack(side=tk.LEFT, padx=6)
        
        self.btn_edit = tk.Button(btn_frame, text="SỬA THÔNG TIN", highlightbackground="#f59e0b", **btn_config)
        self.btn_edit.config(highlightthickness=1, fg="#f59e0b")
        self.btn_edit.pack(side=tk.LEFT, padx=6)
        
        self.btn_delete = tk.Button(btn_frame, text="XÓA", highlightbackground="#ef4444", **btn_config)
        self.btn_delete.config(highlightthickness=1, fg="#ef4444")
        self.btn_delete.pack(side=tk.LEFT, padx=6)
        
        self.btn_export = tk.Button(btn_frame, text="XUẤT EXCEL", highlightbackground="#0ea5e9", **btn_config)
        self.btn_export.config(highlightthickness=1, fg="#0ea5e9")
        self.btn_export.pack(side=tk.LEFT, padx=6)
        
        self.btn_stats = tk.Button(btn_frame, text="THỐNG KÊ BIỂU ĐỒ", highlightbackground="#a855f7", **btn_config)
        self.btn_stats.config(highlightthickness=1, fg="#a855f7") 
        self.btn_stats.pack(side=tk.LEFT, padx=6)
        
        search_frame = tk.Frame(self.root, bg="#0d1622")
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Tìm kiếm (MSV / Họ tên):", font=("Arial", 10), fg="#94a3b8", bg="#0d1622").pack(side=tk.LEFT, padx=5)
        
        self.entry_search = tk.Entry(search_frame, bg="#1e293b", fg="white", insertbackground="white", bd=1, relief="solid", width=25, font=("Arial", 10))
        self.entry_search.pack(side=tk.LEFT, padx=5)
        
        self.btn_search = tk.Button(search_frame, text="TÌM KIẾM", bg="#0284c7", fg="white", font=("Arial", 9, "bold"), bd=0, padx=8, pady=2)
        self.btn_search.pack(side=tk.LEFT, padx=5)
        
        self.btn_reset_search = tk.Button(search_frame, text="HỦY LỌC", bg="#334155", fg="#cbd5e1", font=("Arial", 9, "bold"), bd=0, padx=8, pady=2)
        self.btn_reset_search.pack(side=tk.LEFT, padx=5)

        table_frame = tk.Frame(self.root, bg="#0d1622")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Cyber.Treeview", background="#162235", fieldbackground="#162235", foreground="#f1f5f9", rowheight=28, borderwidth=0)
        style.configure("Cyber.Treeview.Heading", background="#1f2d42", foreground="#38bdf8", font=("Arial", 10, "bold"), borderwidth=0)
        style.map("Cyber.Treeview", background=[('selected', '#0284c7')]) 

        columns = ("MSV", "HoTen", "GioiTinh", "Lop", "SDT", "GPA", "DRL", "KetQua")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Cyber.Treeview")
        
        headers = {"MSV": "MSV", "HoTen": "Họ Tên", "GioiTinh": "Giới tính", "Lop": "Lớp", "SDT": "SDT", "GPA": "GPA", "DRL": "Điểm RL", "KetQua": "Kết Quả"}
        for col, text in headers.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, anchor="center" if col != "HoTen" else "w", width=110 if col in ["HoTen", "KetQua"] else 80)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.tag_configure('dat', foreground="#4ade80", font=("Arial", 10, "bold"))  
        self.tree.tag_configure('truot', foreground="#f87171") 

        self.lbl_stats = tk.Label(self.root, text="Số SV đạt học bổng: 0  |  Số SV không đạt: 0", 
                                  font=("Arial", 11, "bold"), fg="#f59e0b", bg="#0d1622")
        self.lbl_stats.pack(pady=15)

    def create_form_dialog(self, title):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x480")
        dialog.configure(bg="#0d1622")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text=title.upper(), font=("Arial", 14, "bold"), fg="#38bdf8", bg="#0d1622").pack(pady=15)

        form_frame = tk.Frame(dialog, bg="#0d1622")
        form_frame.pack(padx=20, fill=tk.BOTH, expand=True)

        fields = ["MSV", "HoTen", "GioiTinh", "Lop", "SDT", "GPA", "DRL"]
        labels_text = ["Mã Sinh Viên:", "Họ và Tên:", "Giới tính:", "Lớp học:", "Số điện thoại:", "Điểm GPA:", "Điểm Rèn Luyện:"]
        
        entries = {}

        validate_digit = dialog.register(lambda text: text.isdigit() or text == "")
        validate_float = dialog.register(lambda text: text == "" or all(c.isdigit() or c == '.' for c in text) and text.count('.') <= 1)
        validate_alpha = dialog.register(lambda text: text == "" or all(c.isalpha() or c.isspace() for c in text))

        for field, label_text in zip(fields, labels_text):
            row = tk.Frame(form_frame, bg="#0d1622")
            row.pack(fill=tk.X, pady=6)
            
            lbl = tk.Label(row, text=label_text, width=15, anchor="w", fg="#94a3b8", bg="#0d1622", font=("Arial", 10))
            lbl.pack(side=tk.LEFT)

            if field == "GioiTinh":
                var_gender = tk.StringVar(value="Nam")
                ent = ttk.Combobox(row, textvariable=var_gender, values=["Nam", "Nữ"], state="readonly", width=22)
                ent.pack(side=tk.RIGHT, fill=tk.X, expand=True)
                entries[field] = var_gender
            else:
                ent = tk.Entry(row, bg="#1e293b", fg="white", insertbackground="white", bd=1, relief="solid", font=("Arial", 10))
                
                if field in ["GPA", "DRL"]:
                    ent.config(validate="key", validatecommand=(validate_float, '%P'))
                elif field == "SDT":
                    ent.config(validate="key", validatecommand=(validate_digit, '%P'))
                elif field == "HoTen":
                    ent.config(validate="key", validatecommand=(validate_alpha, '%P'))
                
                ent.pack(side=tk.RIGHT, fill=tk.X, expand=True)
                entries[field] = ent

            # Fix dán văn bản bị lỗi font hoặc lỗi bộ lọc phím tắt
            ent.bind("<Control-v>", lambda e: "break")

        btn_save = tk.Button(dialog, text="LƯU THÔNG TIN", bg="#10b981", fg="white", font=("Arial", 10, "bold"), bd=0, pady=8, cursor="hand2")
        btn_save.pack(fill=tk.X, padx=20, pady=20)

        return dialog, entries, btn_save