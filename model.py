import pandas as pd
import re
import os

class StudentModel:
    def __init__(self):
        # Đường dẫn file lưu trữ cục bộ
        self.file_path = 'danh_sach_sinh_vien.csv'
        
        # Tự động nạp dữ liệu cũ từ kho lưu trữ nếu file đã tồn tại
        if os.path.exists(self.file_path):
            try:
                # Ép kiểu 'str' cho MSV, SDT, Lop để tránh việc Pandas tự convert mất số 0 ở đầu
                self.df = pd.read_csv(self.file_path, dtype={'MSV': str, 'SDT': str, 'Lop': str})
            except Exception:
                self.init_empty_df()
        else:
            self.init_empty_df()

    def init_empty_df(self):
        self.df = pd.DataFrame(columns=['MSV', 'HoTen', 'GioiTinh', 'Lop', 'SDT', 'GPA', 'DRL', 'KetQua'])

    def save_to_storage(self):
        """Hàm ghi dữ liệu từ bộ nhớ RAM xuống file lưu trữ vật lý"""
        # Sử dụng mã hóa utf-8-sig để khi mở file bằng Microsoft Excel không bị lỗi font Tiếng Việt
        self.df.to_csv(self.file_path, index=False, encoding='utf-8-sig')

    def validate_data(self, msv, hoten, lop, sdt, gpa_str, drl_str):
        if not all([msv, hoten, lop, sdt, gpa_str, drl_str]):
            return False, "Vui lòng nhập đầy đủ tất cả các trường dữ liệu bắt buộc!"

        pattern_msv = r"^(1[4-9]|2[0-6])(dh|DH)\d{6}$"
        if not re.match(pattern_msv, msv):
            return False, "Mã SV không hợp lệ!\nĐịnh dạng: Khóa (14-26) + 'DH' + 6 số cuối. (Ví dụ: 21DH123456)"

        pattern_name = r"^[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂÂÊÔƠỨỪỬỮỰẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăâêôơứừửữựấẩẫậắằẳẵặẹẻẽềềểỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ\s]+$"
        if not re.match(pattern_name, hoten):
            return False, "Họ và tên chỉ được chứa chữ cái và khoảng trắng!"

        pattern_lop = r"^[a-zA-Z0-9_-]+$"
        if not re.match(pattern_lop, lop):
            return False, "Tên lớp không được chứa ký tự đặc biệt!"

        pattern_sdt = r"^(03|05|07|08|09)\d{8}$"
        if not re.match(pattern_sdt, sdt):
            return False, "Số điện thoại không hợp lệ!\nPhải gồm 10 chữ số và bắt đầu bằng 03, 05, 07, 08 hoặc 09."

        try:
            gpa = float(gpa_str)
            drl = float(drl_str)
            if not (0 <= gpa <= 4.0):
                return False, "GPA phải nằm trong khoảng từ 0.0 đến 4.0!"
            if not (0 <= drl <= 100):
                return False, "Điểm rèn luyện phải nằm trong khoảng từ 0 đến 100!"
        except ValueError:
            return False, "GPA và Điểm RL phải là số thực hợp lệ!"

        return True, "Hợp lệ"

    def clean_name(self, name):
        words = name.strip().split()
        return " ".join([w.capitalize() for w in words])

    def calculate_scholarship(self, gpa, drl):
        is_eligible = (gpa >= 3.2 and drl >= 80) or (gpa >= 3.6)
        return "Đạt học bổng" if is_eligible else "Không đạt"

    def add_student(self, data):
        data['HoTen'] = self.clean_name(data['HoTen'])
        data['Lop'] = data['Lop'].strip().upper()
        data['KetQua'] = self.calculate_scholarship(float(data['GPA']), float(data['DRL']))
        new_df = pd.DataFrame([data])
        self.df = pd.concat([self.df, new_df], ignore_index=True)
        
        # 🌟 ĐỒNG BỘ XUỐNG KHO LƯU TRỮ TRỰC TIẾP
        self.save_to_storage()

    def update_student(self, msv_old, new_data):
        new_data['HoTen'] = self.clean_name(new_data['HoTen'])
        new_data['Lop'] = new_data['Lop'].strip().upper()
        new_data['KetQua'] = self.calculate_scholarship(float(new_data['GPA']), float(new_data['DRL']))
        idx = self.df.index[self.df['MSV'] == msv_old].tolist()
        if idx:
            for key, value in new_data.items():
                self.df.at[idx[0], key] = value
            
            # 🌟 ĐỒNG BỘ XUỐNG KHO LƯU TRỮ TRỰC TIẾP
            self.save_to_storage()

    def delete_student(self, msv):
        self.df = self.df[self.df['MSV'] != msv].reset_index(drop=True)
        
        # 🌟 ĐỒNG BỘ XUỐNG KHO LƯU TRỮ TRỰC TIẾP
        self.save_to_storage()

    def search_students(self, query):
        if not query:
            return self.df
        query = query.lower()
        # Tìm kiếm trực tiếp trên DataFrame đã nạp từ kho lưu trữ
        filtered_df = self.df[
            self.df['MSV'].astype(str).str.lower().str.contains(query) | 
            self.df['HoTen'].astype(str).str.lower().str.contains(query)
        ]
        return filtered_df

    def export_to_excel(self, file_path):
        self.df.to_excel(file_path, index=False)