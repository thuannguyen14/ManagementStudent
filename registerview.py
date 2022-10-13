import tkinter as tk
from tkinter.messagebox import showerror, showinfo, askyesno
import numpy as np
import matplotlib.pyplot as plt
from controller.registercontroller import RegisterController
from controller.studentcontroller import StudentController
from controller.subjectcontroller import SubjectController
from utils import *


class RegisterView:
    def __init__(self, master):
        super().__init__()
        self.img_register = None
        self.img_cancel = None
        self.btn_register = None
        self.btn_cancel = None
        self.combobox_subject_id = None
        self.entry_student_id = None
        self.btn_statistic = None
        self.img_statistic = None
        self.img_chart = None
        self.btn_draw_chart = None
        self.frame = master
        self.btn_search = None
        self.search_entry = None
        self.search_var = None
        self.img_search = None
        self.sort_var = None
        self.tbl_register = None
        self.btn_remove = None
        self.img_remove = None
        self.btn_edit = None
        self.img_edit = None
        self.btn_reload = None
        self.img_refresh = None
        self.subjects = []
        self.students = []
        self.registers = []
        self.controller = RegisterController()
        self.create_widgets()
        self.create_buttons()
        self.load_data()

    def create_widgets(self):
        columns = ('reg_id', 'subject_id', 'subject_name', 'student_id',
                   'student_name', 'reg_time')
        self.tbl_register = ttk.Treeview(self.frame, columns=columns,
                                         show='headings', height=10)
        self.tbl_register.grid(row=0, column=0, columnspan=3,
                               sticky=tk.NSEW, pady=4, padx=4)
        set_style(self.tbl_register)
        # show heading
        self.tbl_register.heading('reg_id', text='Mã đăng ký')
        self.tbl_register.heading('subject_id', text='Mã môn học')
        self.tbl_register.heading('subject_name', text='Tên môn học')
        self.tbl_register.heading('student_id', text='Mã sinh viên')
        self.tbl_register.heading('student_name', text='Họ và tên')
        self.tbl_register.heading('reg_time', text='Thời gian đăng ký')
        # config columns
        self.tbl_register.column(0, stretch=tk.NO, width=120, anchor=tk.CENTER)
        self.tbl_register.column(1, stretch=tk.NO, width=160, anchor=tk.W)
        self.tbl_register.column(2, stretch=tk.NO, width=220, anchor=tk.W)
        self.tbl_register.column(3, stretch=tk.NO, width=160, anchor=tk.CENTER)
        self.tbl_register.column(4, stretch=tk.NO, width=220, anchor=tk.W)
        self.tbl_register.column(5, stretch=tk.NO, width=220, anchor=tk.W)
        # add scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL,
                                  command=self.tbl_register.yview)
        scrollbar.grid(row=0, column=3, sticky=tk.NS)
        self.tbl_register['yscrollcommand'] = scrollbar.set
        # add buttons
        self.create_search_frame()
        self.create_sort_frame()
        self.create_register_frame()

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
        ttk.Combobox(frm_search, values=search_register_criterias,
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
        frm_sort = ttk.LabelFrame(self.frame, text='Sắp xếp bản đăng ký')
        frm_sort.columnconfigure(0, weight=1, uniform='fred')
        frm_sort.columnconfigure(1, weight=1, uniform='fred')
        frm_sort.grid(row=1, column=1, sticky=tk.NSEW, pady=4, padx=4)
        # add radio button to this frame
        ttk.Radiobutton(frm_sort, text='Thứ tự đăng ký sớm-muộn', value=1,
                        variable=self.sort_var,
                        command=self.item_sort_by_register_time_asc). \
            grid(row=0, column=0, pady=4, padx=4, sticky=tk.W)
        ttk.Radiobutton(frm_sort, text='Thứ tự đăng ký muộn-sớm',
                        value=2, variable=self.sort_var,
                        command=self.item_sort_by_register_time_desc). \
            grid(row=1, column=0, pady=4, padx=4, sticky=tk.W)
        ttk.Radiobutton(frm_sort, text='Theo mã môn học tăng dần',
                        value=3, variable=self.sort_var,
                        command=self.item_sort_by_subject_id_selected). \
            grid(row=0, column=1, pady=4, padx=4, sticky=tk.W)
        ttk.Radiobutton(frm_sort, text='Theo mã sinh viên tăng dần',
                        value=4, variable=self.sort_var,
                        command=self.item_sort_by_student_id_selected). \
            grid(row=1, column=1, pady=4, padx=4, sticky=tk.W)

    def create_register_frame(self):
        frm_add_new_register = ttk.LabelFrame(self.frame, text='Đăng ký môn học')
        # config set all columns have same width space
        frm_add_new_register.columnconfigure(0, weight=1, uniform='fred')
        frm_add_new_register.columnconfigure(1, weight=1, uniform='fred')
        frm_add_new_register.rowconfigure(0, weight=1, uniform='fred')
        frm_add_new_register.rowconfigure(1, weight=1, uniform='fred')
        frm_add_new_register.rowconfigure(2, weight=1, uniform='fred')
        frm_add_new_register.grid(row=1, column=2, sticky=tk.NSEW, pady=4, padx=4)
        # add combobox, entry and button
        self.entry_student_id = ttk.Entry(frm_add_new_register, width=15)
        self.combobox_subject_id = ttk.Combobox(frm_add_new_register, width=12)
        # add button
        self.img_cancel = tk.PhotoImage(file='view/assets/remove.png')
        self.btn_cancel = ttk.Button(frm_add_new_register, text='Hủy bỏ', width=15,
                                     command=self.btn_cancel_clicked,
                                     image=self.img_cancel, compound=tk.LEFT)
        self.img_register = tk.PhotoImage(file='view/assets/add.png')
        self.btn_register = ttk.Button(frm_add_new_register, text='Đăng ký', width=15,
                                       command=self.btn_register_clicked,
                                       image=self.img_register, compound=tk.LEFT)
        # add label
        ttk.Label(frm_add_new_register, text='Mã sinh viên:'). \
            grid(row=0, column=0, padx=16, pady=4, sticky=tk.W)
        ttk.Label(frm_add_new_register, text='Mã môn học:'). \
            grid(row=1, column=0, padx=16, pady=4, sticky=tk.W)
        # put into grid
        self.entry_student_id.grid(row=0, column=1, pady=4, padx=16, sticky=tk.EW)
        self.combobox_subject_id.grid(row=1, column=1, pady=4, padx=16, sticky=tk.EW)
        self.btn_register.grid(row=2, column=1, pady=4, padx=16)
        self.btn_cancel.grid(row=2, column=0, pady=4, padx=16)

    def create_buttons(self):
        button_frame = ttk.LabelFrame(self.frame, text='Các thao tác')
        button_frame.columnconfigure(0, weight=1, uniform='fred')
        button_frame.columnconfigure(1, weight=1, uniform='fred')
        button_frame.columnconfigure(2, weight=1, uniform='fred')
        button_frame.columnconfigure(3, weight=1, uniform='fred')
        button_frame.grid(row=2, column=0, columnspan=3,
                          padx=4, pady=4, sticky=tk.NSEW)
        self.img_refresh = tk.PhotoImage(file='view/assets/refresh.png')
        self.btn_reload = ttk.Button(button_frame, text='Làm mới', width=20,
                                     command=self.load_data, image=self.img_refresh,
                                     compound=tk.LEFT)
        self.btn_reload.grid(row=0, column=0, pady=4, padx=4)
        self.img_remove = tk.PhotoImage(file='view/assets/remove.png')
        self.btn_remove = ttk.Button(button_frame, text='Xóa bỏ', width=20,
                                     command=self.btn_remove_clicked,
                                     image=self.img_remove, compound=tk.LEFT)
        self.btn_remove.grid(row=0, column=1, pady=4, padx=4)
        chart_icon_path = 'view/assets/chart.png'
        stat_icon_path = 'view/assets/stat.png'
        self.img_chart = tk.PhotoImage(file=chart_icon_path)
        self.img_statistic = tk.PhotoImage(file=stat_icon_path)
        self.btn_statistic = ttk.Button(button_frame, text='Thống kê',
                                        image=self.img_statistic, compound=tk.LEFT,
                                        command=self.btn_statistic_clicked, width=15)
        self.btn_draw_chart = ttk.Button(button_frame, text='Vẽ biểu đồ',
                                         image=self.img_chart, compound=tk.LEFT,
                                         command=self.btn_draw_chart_clicked, width=15)
        self.btn_statistic.grid(row=0, column=2, padx=4, pady=4)
        self.btn_draw_chart.grid(row=0, column=3, padx=4, pady=4)

    def load_data(self, should_show=True):
        self.subjects.clear()
        self.students.clear()
        if len(self.subjects) == 0:
            self.students = StudentController().read_file(STUDENT_FILE_NAME)
            self.subjects = SubjectController().read_file(SUBJECT_FILE_NAME)
            # bind data to combobox that contain subject_id
            subject_ids = get_subject_id(self.subjects)
            self.combobox_subject_id.configure(values=subject_ids)
        self.registers = self.controller.read_file(REGISTER_FILE_NAME, self.students, self.subjects)
        if should_show:
            self.show_registers()

    def show_registers(self):
        clear_treeview(self.tbl_register)
        index = 1
        self.tbl_register.selection_clear()
        for register in self.registers:
            if index % 2 == 0:
                tag = 'even'
            else:
                tag = 'odd'
            self.tbl_register.insert('', tk.END,
                                     values=register_to_tuple(register),
                                     tags=(tag,), iid=f'{index - 1}')
            index += 1

    def btn_statistic_clicked(self):
        pairs = self.controller.statistic(self.registers)
        self.show_table(pairs)

    def btn_cancel_clicked(self):
        self.entry_student_id.delete(0, 'end')
        self.combobox_subject_id.delete(0, 'end')

    def btn_register_clicked(self):
        student_id = self.entry_student_id.get().upper()
        subject_id_str = self.combobox_subject_id.get()
        if student_id.strip() == '':
            showerror('Student Id Error', 'Student id cannot be blank!')
        elif subject_id_str == '':
            showerror('Subject Id Error', 'Subject id cannot be empty!')
        else:
            subject_id = int(subject_id_str.strip())
            subject = self.controller.get_subject_by_id(self.subjects, subject_id)
            student = self.controller.get_student_by_id(self.students, student_id)
            if student is None:
                showerror('Student Id Invalid', 'Incorrect student id. Please check again.')
            elif self.controller.is_register_duplicated(self.registers, student, subject):
                showerror('Record Duplicated', 'This subject has been registered!')
            else:
                register = self.controller.add_register(0, subject, student)
                self.registers.append(register)
                self.show_registers()
                message = f'Student id {student_id} registed subject id {subject_id} successfully!'
                showinfo('Success', message)

    def btn_draw_chart_clicked(self):
        pairs = self.controller.statistic(self.registers)
        labels, data = self.controller.create_stat_data(pairs)
        num_of_student = np.array(data)
        colors = ['#94e368', '#9255e3', '#3b88f5', '#14cfff', '#f1ff14', '#ABEBC6',
                  '#707B7C', '#14E4F1', '#1443F1', '#C8D2F7', '#F9F7A2', '#CEF9A2',
                  '#80FA05', '#EFB9C4', '#EFB9E9', '#110E63']
        explode = [0.0] * len(data)
        explode[0] = 0.1
        plt.pie(num_of_student, colors=colors, labels=labels, explode=explode,
                shadow=True, startangle=30, autopct='%1.1f%%',
                textprops={'color': '#ff0000'})
        # set title
        plt.title('Biểu đồ phân bố đăng ký môn học')
        # add legend
        plt.legend(loc='lower right', title='Mã môn học:', bbox_to_anchor=(1.25, 0))
        plt.show()

    def btn_remove_clicked(self):
        registers = self.controller.read_file(REGISTER_FILE_NAME, self.students, self.subjects)
        item_selected = self.tbl_register.selection()
        if len(item_selected) > 0:
            title = 'Confirmation'
            message = 'Do you want to delete item(s) selected?'
            ans = askyesno(title, message)
            if ans:
                index = int(item_selected[0])
                register_id = self.registers[index].register_id
                self.controller.remove(self.registers, register_id)  # xóa phần tử trong danh sách sinh viên
                self.controller.remove(registers, register_id)  # xóa phần tử trong danh sách nguyên bản
                self.tbl_register.delete(item_selected[0])  # xóa phần tử trong bảng
                self.controller.write_file(REGISTER_FILE_NAME, registers)  # update file
                showinfo(title='Infomation', message=f'Delete register id "{register_id}" successfully!')
        else:
            showerror(title='Error', message='Please select a register to delete first!')

    def item_save_selected(self):
        self.controller.write_file(REGISTER_FILE_NAME, self.registers)

    def btn_search_clicked(self):
        key = self.search_entry.get()
        criteria = self.search_var.get()
        if len(key) == 0:
            showerror('Invalid keyword', 'Please enter keyword first!')
        elif len(criteria) == 0:
            showerror('Invalid criteria', 'Please select criteria to search!')
        else:
            if criteria == search_register_criterias[0]:
                if is_student_id_valid(key):
                    self.find_by_student_id(key)
                else:
                    showerror('Invalid student id', 'Student id must in the form SV####')
            elif criteria == search_register_criterias[1]:
                if is_subject_id_valid(key):
                    self.find_by_subject_id(int(key))
                else:
                    showerror('Invalid subject_id', 'Subject id must be integer number 4 digits')

    def item_sort_by_register_time_asc(self):
        self.controller.sort_by_register_time_asc(self.registers)
        self.show_registers()

    def item_sort_by_register_time_desc(self):
        self.controller.sort_by_register_time_desc(self.registers)
        self.show_registers()

    def item_sort_by_subject_id_selected(self):
        self.controller.sort_by_subject_id(self.registers)
        self.show_registers()

    def item_sort_by_student_id_selected(self):
        self.controller.sort_by_student_id(self.registers)
        self.show_registers()

    def find_by_student_id(self, key: str):
        self.load_data(False)  # reload data from file
        result = self.controller.find_by_student_id(self.registers, key)
        self.check_result(result)

    def find_by_subject_id(self, key: int):
        self.load_data(False)  # reload subject
        result = self.controller.find_by_subject_id(self.registers, key)
        self.check_result(result)

    def check_result(self, result: list[Register]):
        if len(result) == 0:
            self.registers.clear()
            self.show_registers()
            showinfo('Search Result', 'No result found!')
        else:
            self.registers.clear()
            self.registers = result.copy()
            self.show_registers()

    def show_table(self, pairs):
        frm_stat = tk.Tk()
        frm_stat.title('Statistic Student Register Window')
        frm_stat.resizable(False, False)
        ttk.Button(text='OK', master=frm_stat, command=frm_stat.destroy). \
            grid(row=1, column=0, padx=16, pady=4, sticky=tk.EW)
        columns = ('row_number', 'subject_id', 'subject_name', 'number_register')
        tbl_stat = ttk.Treeview(frm_stat, columns=columns, show='headings', height=10)
        tbl_stat.grid(row=0, column=0, sticky=tk.EW, pady=4, padx=4)
        # set style
        set_style(tbl_stat, theme='default')
        # show heading
        tbl_stat.heading('row_number', text='STT')
        tbl_stat.heading('subject_id', text='Mã môn học')
        tbl_stat.heading('subject_name', text='Tên môn học')
        tbl_stat.heading('number_register', text='Số lượng đăng ký')
        # config columns
        tbl_stat.column(0, stretch=tk.NO, width=100, anchor=tk.CENTER)
        tbl_stat.column(1, stretch=tk.NO, width=100, anchor=tk.CENTER)
        tbl_stat.column(2, stretch=tk.NO, width=160, anchor=tk.W)
        tbl_stat.column(3, stretch=tk.NO, width=100, anchor=tk.CENTER)
        # add scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL,
                                  command=tbl_stat.yview)
        scrollbar.grid(row=0, column=3, sticky=tk.NS)
        tbl_stat['yscrollcommand'] = scrollbar.set
        # add data
        _fill_stat_data(tbl_stat, pairs)
        frm_stat.mainloop()


def _fill_stat_data(tbl, pairs):
    clear_treeview(tbl)
    index = 1
    tbl.selection_clear()
    for pair in pairs:
        if index % 2 == 0:
            tag = 'even'
        else:
            tag = 'odd'
        row_data = (index, pair.subject.subject_id, pair.subject.subject_name, pair.number_of_register)
        tbl.insert('', tk.END, values=row_data,
                   tags=(tag,), iid=f'{index - 1}')
        index += 1