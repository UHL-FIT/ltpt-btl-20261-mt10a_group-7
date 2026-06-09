import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StudentStatistic:
    def __init__(self, parent, model):
        self.parent = parent
        self.model = model
        
        self.window = tk.Toplevel(self.parent)
        self.window.title("Hệ thống Phân tích Học bổng 2026")
        self.window.geometry("1100x700")
        self.window.configure(bg="#0d1622")
        self.window.grab_set()

        # Tiêu đề
        tk.Label(self.window, text="HỆ THỐNG PHÂN TÍCH BIỂU ĐỒ HỌC BỔNG", 
                 font=("Arial", 16, "bold"), fg="#38bdf8", bg="#0d1622").pack(pady=10)

        # Thanh lọc
        filter_frame = tk.Frame(self.window, bg="#0d1622")
        filter_frame.pack(pady=5)
        
        tk.Label(filter_frame, text="Lọc theo Lớp:", fg="white", bg="#0d1622").pack(side=tk.LEFT)
        
        # Khởi tạo Combobox
        self.cb_class = ttk.Combobox(filter_frame, state="readonly")
        self.cb_class.pack(side=tk.LEFT, padx=10)
        self.cb_class.bind("<<ComboboxSelected>>", lambda e: self.generate_report())

        # Khung chứa
        self.main_container = tk.Frame(self.window, bg="#0d1622")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.left_panel = tk.Frame(self.main_container, bg="#162235", width=300)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        self.right_panel = tk.Frame(self.main_container, bg="#0d1622")
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Cài đặt danh sách lớp ban đầu
        self.update_combobox_list()
        self.cb_class.set("Tất cả")

        self.generate_report()

    def update_combobox_list(self):
        """Hàm tự quét kho dữ liệu để nạp các lớp hiện có vào Combobox"""
        current_val = self.cb_class.get()
        unique_classes = sorted(list(self.model.df['Lop'].dropna().unique()))
        all_options = ["Tất cả"] + unique_classes
        self.cb_class['values'] = all_options
        if current_val in all_options:
            self.cb_class.set(current_val)
        else:
            self.cb_class.set("Tất cả")

    def generate_report(self):
        # Đồng bộ lại danh sách lớp phòng trường hợp có lớp mới vừa được thêm
        self.update_combobox_list()

        # 1. Lọc dữ liệu
        df = self.model.df
        selected_class = self.cb_class.get()
        if selected_class != "Tất cả" and selected_class != "":
            df = df[df['Lop'] == selected_class]

        # 2. Xóa widget cũ
        for widget in self.left_panel.winfo_children(): widget.destroy()
        for widget in self.right_panel.winfo_children(): widget.destroy()

        # 3. Tính toán số liệu
        total_sv = len(df)
        df_hb = df[df['KetQua'] == "Đạt học bổng"]
        total_hb = len(df_hb)
        
        # Hiển thị số liệu cột trái
        tk.Label(self.left_panel, text="📊 SỐ LIỆU CHUNG", fg="#10b981", bg="#162235", font=("Arial",12,"bold")).pack(pady=10)
        tk.Label(self.left_panel, text=f"Tổng số SV: {total_sv}", fg="white", bg="#162235").pack()
        tk.Label(self.left_panel, text=f"Tổng đạt HB: {total_hb}", fg="white", bg="#162235").pack()

        if not df.empty:
            try:
                top_student = df.loc[df['GPA'].astype(float).idxmax()]
                tk.Label(self.left_panel, text="🏆 THỦ KHOA", fg="#f59e0b", bg="#162235", font=("Arial",12,"bold")).pack(pady=20)
                tk.Label(self.left_panel, text=top_student['HoTen'], fg="#38bdf8", bg="#162235").pack()
                tk.Label(self.left_panel, text=f"GPA: {top_student['GPA']}", fg="#f59e0b", bg="#162235").pack()
            except Exception:
                pass

        # 4. Vẽ biểu đồ
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8), facecolor='#0d1622')
        
        # Biểu đồ Tròn
        if total_sv > 0:
            ax1.pie([len(df_hb), total_sv-total_hb], labels=['Đạt', 'Trượt'], colors=['#10b981', '#ef4444'], autopct='%1.1f%%', textprops={'color':'white'})
            ax1.set_title("Tỷ lệ đạt học bổng", color="white")
        else:
            ax1.text(0.5, 0.5, "Không có dữ liệu", color="white", ha='center', va='center')
        
        # Biểu đồ Cột
        classes = df['Lop'].unique()
        if len(classes) > 0:
            counts = [len(df[(df['Lop']==c) & (df['KetQua']=="Đạt học bổng")]) for c in classes]
            ax2.bar(classes, counts, color='#38bdf8')
            ax2.set_title("Số SV đạt HB theo lớp", color="white")
            ax2.tick_params(colors='white')
        else:
            ax2.text(0.5, 0.5, "Không có dữ liệu", color="white", ha='center', va='center')

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.right_panel)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)