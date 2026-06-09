import tkinter as tk
from model import StudentModel  
from view import StudentView
from controller import StudentController

def main():
    root = tk.Tk()
    
    # 1. Khởi tạo Model (Tự động nạp dữ liệu từ file CSV lên)
    model = StudentModel()
    
    # 2. Khởi tạo View
    view = StudentView(root)
    
    # 3. Khởi tạo Controller 
    controller = StudentController(model, view)
    
    # 4. Thiết lập tham chiếu ngược
    view.controller = controller
    
    root.mainloop()

if __name__ == "__main__":
    main()