import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter.messagebox import showerror, askyesno, showinfo
from utils import *
from controller.studentcontroller import StudentController
from view.editstudentview import EditStudentView


class StudentView:
    def __init__(self, frame):
        super().__init__()
        self.img_refresh = None
        self.btn_reload = None
        self.img_remove = None
        self.btn_remove = None
        self.img_chart = None
        self.btn_edit = None
        self.img_edit = None
        self.btn_draw_chart = None
        self.search_entry = None
        self.search_var = None
        self.sort_var = None
        self.img_search = None
        self.btn_search = None
        self.tbl_student = None
        self.frame = frame
        self.students = []
        self.controller = StudentController()
        self.create_widgets()
        self.load_student()

    def create_widgets(self):
        columns = ('id', 'full_name', 'birth_date',
                   'student_id', 'email', 'address', 'gpa', 'major')
        self.tbl_student = ttk.Treeview(self.frame, columns=columns,
                                        show='headings', height=10)
        self.tbl_student.grid(row=0, column=0, columnspan=3,
                              sticky=tk.NSEW, pady=4, padx=4)
        # set style for the view
        set_style(self.tbl_student)
        # show heading
        self.tbl_student.heading('id', text='CMND/CCCD')
        self.tbl_student.heading('full_name', text='Họ và tên')
        self.tbl_student.heading('birth_date', text='Ngày sinh')
        self.tbl_student.heading('student_id', text='Mã SV')
        self.tbl_student.heading('email', text='Email')
        self.tbl_student.heading('address', text='Địa chỉ')
        self.tbl_student.heading('gpa', text='Điểm TB')
        self.tbl_student.heading('major', text='Chuyên ngành')
        # config columns
        self.tbl_student.column(0, stretch=tk.NO, width=100, anchor=tk.CENTER)
        self.tbl_student.column(1, stretch=tk.NO, width=150, anchor=tk.W)
        self.tbl_student.column(2, stretch=tk.NO, width=100, anchor=tk.CENTER)
        self.tbl_student.column(3, stretch=tk.NO, width=100, anchor=tk.CENTER)
        self.tbl_student.column(4, stretch=tk.NO, width=180, anchor=tk.W)
        self.tbl_student.column(5, stretch=tk.NO, width=220, anchor=tk.W)
        self.tbl_student.column(6, stretch=tk.NO, width=100, anchor=tk.CENTER)
        self.tbl_student.column(7, stretch=tk.NO, width=150, anchor=tk.W)
        # add scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL,
                                  command=self.tbl_student.yview)
        scrollbar.grid(row=0, column=3, sticky=tk.NS)
        self.tbl_student['yscrollcommand'] = scrollbar.set
        # add buttons
        self.create_search_frame()
        self.create_sort_frame()
        self.create_chart_frame()
        self.create_buttons()

    def create_search_frame(self):
        self.search_var = tk.StringVar()
        frm_search = ttk.LabelFrame(self.frame, text='Tìm kiếm')
        # config set all columns have same width space
        frm_search.columnconfigure(0, weight=1, uniform='fred')
        frm_search.columnconfigure(1, weight=1, uniform='fred')
        frm_search.grid(row=1, column=0, sticky=tk.NSEW, pady=4, padx=4)
        # add combobox
        ttk.Label(frm_search, text='Tiêu chí tìm kiếm:'). \
            grid(row=0, column=0, sticky=tk.W, pady=4, padx=4)
        ttk.Combobox(frm_search, values=search_student_criterias,
                     textvariable=self.search_var). \
            grid(row=1, column=0, padx=4, pady=4, sticky=tk.W,
                 ipady=4, ipadx=4)
        # add search part
        ttk.Label(frm_search, text='Từ khóa:'). \
            grid(row=0, column=1, sticky=tk.W, padx=4, pady=4)
        self.search_entry = ttk.Entry(frm_search)
        self.search_entry.grid(row=1, column=1, sticky=tk.EW, padx=4, pady=4,
                               ipadx=4, ipady=4)
        path = 'view/assets/search_24.png'
        self.img_search = tk.PhotoImage(file=path)
        self.btn_search = ttk.Button(frm_search, text='Tìm kiếm',
                                     image=self.img_search, compound=tk.LEFT,
                                     command=self.btn_search_clicked, width=15)
        self.btn_search.grid(row=2, column=1, padx=4, pady=4)

    def create_sort_frame(self):
        self.sort_var = tk.IntVar(value=0)
        frm_sort = ttk.LabelFrame(self.frame, text='Sắp xếp')
        frm_sort.columnconfigure(0, weight=1, uniform='fred')
        frm_sort.columnconfigure(1, weight=1, uniform='fred')
        frm_sort.grid(row=1, column=1, sticky=tk.NSEW, pady=4, padx=4)
        # add radio button to this frame
        ttk.Radiobutton(frm_sort, text='Theo tên a-z', value=1,
                        variable=self.sort_var,
                        command=self.item_sort_by_name_selected). \
            grid(row=0, column=0, pady=4, padx=4, sticky=tk.W)
        ttk.Radiobutton(frm_sort, text='Theo ngày sinh',
                        value=2, variable=self.sort_var,
                        command=self.item_sort_by_birth_date_selected). \
            grid(row=1, column=0, pady=4, padx=4, sticky=tk.W)
        ttk.Radiobutton(frm_sort, text='Theo điểm TB',
                        value=3, variable=self.sort_var,
                        command=self.item_sort_by_gpa_selected). \
            grid(row=0, column=1, pady=4, padx=4, sticky=tk.W)
        ttk.Radiobutton(frm_sort, text='Theo điểm và Họ tên',
                        value=4, variable=self.sort_var,
                        command=self.item_sort_by_gpa_and_name_selected). \
            grid(row=1, column=1, pady=4, padx=4, sticky=tk.W)

    def create_chart_frame(self):
        frm_other = ttk.LabelFrame(self.frame, text='Biểu đồ')
        frm_other.grid(row=1, column=2, sticky=tk.NSEW, pady=4, padx=4)
        self.img_chart = tk.PhotoImage(file='view/assets/chart.png')
        self.btn_draw_chart = ttk.Button(frm_other, text='Vẽ biểu đồ', width=20,
                                         command=lambda: self.draw_chart(),
                                         image=self.img_chart, compound=tk.LEFT)
        self.btn_draw_chart.place(rely=0.5, relx=0.5, anchor=tk.CENTER)

    def create_buttons(self):
        button_frame = ttk.LabelFrame(self.frame, text='Các thao tác')
        button_frame.columnconfigure(0, weight=1, uniform='fred')
        button_frame.columnconfigure(1, weight=1, uniform='fred')
        button_frame.columnconfigure(2, weight=1, uniform='fred')
        button_frame.grid(row=2, column=0, columnspan=3,
                          padx=4, pady=4, sticky=tk.NSEW)
        self.img_refresh = tk.PhotoImage(file='view/assets/refresh.png')
        self.btn_reload = ttk.Button(button_frame, text='Làm mới', width=20,
                                     command=self.load_student, image=self.img_refresh,
                                     compound=tk.LEFT)
        self.btn_reload.grid(row=0, column=0, ipady=4, ipadx=4, pady=4, padx=4)
        self.img_edit = tk.PhotoImage(file='view/assets/editing.png')
        self.btn_edit = ttk.Button(button_frame, text='Sửa điểm TB', width=20,
                                   command=self.btn_edit_student_clicked,
                                   image=self.img_edit, compound=tk.LEFT)
        self.btn_edit.grid(row=0, column=1, ipady=4, ipadx=4, pady=4, padx=4)
        self.img_remove = tk.PhotoImage(file='view/assets/remove.png')
        self.btn_remove = ttk.Button(button_frame, text='Xóa bỏ', width=20,
                                     command=self.btn_remove_student_clicked,
                                     image=self.img_remove, compound=tk.LEFT)
        self.btn_remove.grid(row=0, column=2, ipadx=4, ipady=4, pady=4, padx=4)

    def load_student(self, should_show=True):
        self.students.clear()
        self.students = self.controller.read_file(STUDENT_FILE_NAME)
        if should_show:
            self.show_students()

    def show_students(self):
        clear_treeview(self.tbl_student)
        index = 1
        self.tbl_student.selection_clear()
        for student in self.students:
            if index % 2 == 0:
                tag = 'even'
            else:
                tag = 'odd'
            self.tbl_student.insert('', tk.END,
                                    values=student_to_tuple(student),
                                    tags=(tag,), iid=f'{index-1}')
            index += 1

    def btn_remove_student_clicked(self):
        students = self.controller.read_file(STUDENT_FILE_NAME)
        item_selected = self.tbl_student.selection()
        if len(item_selected) > 0:
            title = 'Confirmation'
            message = 'Do you want to delete item(s) selected?'
            ans = askyesno(title, message)
            if ans:
                index = int(item_selected[0])
                student_id = self.students[index].student_id
                self.controller.remove(self.students, student_id)  # xóa phần tử trong danh sách sinh viên
                self.controller.remove(students, student_id)  # xóa phần tử trong danh sách nguyên bản
                self.tbl_student.delete(item_selected[0])  # xóa phần tử trong bảng
                self.controller.write_file(STUDENT_FILE_NAME, students)  # update file
                showinfo(title='Infomation', message=f'Delete student id "{student_id}" successfully!')
        else:
            showerror(title='Error', message='Please select a student to delete first!')

    def btn_edit_student_clicked(self):
        item_selected = self.tbl_student.selection()
        if len(item_selected) > 0:
            index = int(item_selected[0])  # convert iid from str to int
            EditStudentView(self, self.students[index]).attributes('-topmost', True)
        else:
            showerror(title='Error', message='Please select a student to edit first!')

    def item_create_student_selected(self, student: Student):
        self.students.append(student)
        self.show_students()

    def item_sort_by_name_selected(self):
        self.controller.sort_by_name(self.students)
        # self.students.sort(key=lambda x: (x.full_name.first_name, x.full_name.last_name))
        self.show_students()

    def item_sort_by_birth_date_selected(self):
        self.controller.sort_by_birth_date(self.students)
        self.show_students()

    def item_sort_by_gpa_selected(self):
        self.controller.sort_by_gpa(self.students)
        self.show_students()

    def item_sort_by_gpa_and_name_selected(self):
        self.controller.sort_by_name_gpa(self.students)
        self.show_students()

    def item_save_selected(self):
        self.controller.write_file(STUDENT_FILE_NAME, students=self.students)

    def draw_chart(self):
        caps, stat = self.controller.statistic_capacity(self.students)
        num_of_student = np.array(stat)
        colors = ['#94e368', '#9255e3', '#3b88f5', '#14cfff', '#f1ff14']
        explode = [0.1, 0.05, 0, 0, 0]
        plt.pie(num_of_student, colors=colors, labels=caps, explode=explode,
                shadow=True, startangle=30, autopct='%1.2f%%',
                textprops={'color': '#ff0000'})
        # set title
        plt.title('Biểu đồ học lực sinh viên')
        # add legend
        plt.legend(loc='lower right', title='Học lực:', bbox_to_anchor=(1.25, 0))
        plt.show()

    def btn_search_clicked(self):
        key = self.search_entry.get()
        criteria = self.search_var.get()
        if len(key) == 0:
            showerror('Invalid keyword', 'Please enter keyword first!')
        elif len(criteria) == 0:
            showerror('Invalid criteria', 'Please select criteria to search!')
        else:
            if criteria == search_student_criterias[0]:
                self.search_by_name(key)
            elif criteria == search_student_criterias[1]:
                if is_gpa_valid(key):
                    gpa = float(key)
                    if gpa < 0 or gpa > 4.0:
                        showerror('Invalid GPA', 'GPA must in range [0, 4.0]')
                    else:
                        self.search_by_gpa(gpa)
                else:
                    showerror('Invalid GPA', 'GPA must be number from 0.0 to 4.0')
            elif criteria == search_student_criterias[2]:
                if is_date_valid(key):
                    day = int(key)
                    if day < 1 or day > 31:
                        showerror('Invalid day', 'Day must in range [1, 31]')
                    else:
                        self.search_by_birth_date(day)
                else:
                    showerror('Invalid day', 'Day must be number from 1 to 31')
            elif criteria == search_student_criterias[3]:
                if is_date_valid(key):
                    month = int(key)
                    if month < 1 or month > 12:
                        showerror('Invalid day', 'Day must in range [1, 31]')
                    else:
                        self.search_by_birth_month(month)
                else:
                    showerror('Invalid month', 'Month must be number from 1 to 12')
            elif criteria == search_student_criterias[4]:
                if is_date_valid(key):
                    year = int(key)
                    if year < 1900 or year > 2030:
                        showerror('Invalid year', 'Day must in range [1, 31]')
                    else:
                        self.search_by_birth_year(year)
                else:
                    showerror('Invalid year', 'Year must be number from 1900 to 2030')

    def search_by_name(self, key: str):
        self.load_student(False)  # reload student
        result = self.controller.search_by_name(self.students, key)
        self.check_result(result)

    def search_by_gpa(self, key: float):
        self.load_student(False)  # reload student
        result = self.controller.search_by_gpa(self.students, key)
        self.check_result(result)

    def search_by_birth_date(self, key: int):
        self.load_student(False)  # reload student
        result = self.controller.search_by_birth_date(self.students, key)
        self.check_result(result)

    def search_by_birth_month(self, key: int):
        self.load_student(False)  # reload student
        result = self.controller.search_by_birth_month(self.students, key)
        self.check_result(result)

    def search_by_birth_year(self, key: int):
        self.load_student(False)  # reload student
        result = self.controller.search_by_birth_year(self.students, key)
        self.check_result(result)

    def check_result(self, result: list[Student]):
        if len(result) == 0:
            self.students.clear()
            self.show_students()
            showinfo('Search Result', 'No result found!')
        else:
            self.students.clear()
            self.students = result.copy()
            self.show_students()