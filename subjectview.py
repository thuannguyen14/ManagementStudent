import tkinter as tk
from tkinter.messagebox import showerror, showinfo, askyesno

from controller.subjectcontroller import SubjectController
from error.exceptions import SubjectLessonError, SubjectCreditError
from utils import *


class SubjectView:
    def __init__(self, frame):
        super().__init__()
        self.btn_search = None
        self.search_entry = None
        self.search_var = None
        self.img_search = None
        self.sort_var = None
        self.tbl_subject = None
        self.btn_remove = None
        self.img_remove = None
        self.btn_edit = None
        self.img_edit = None
        self.btn_reload = None
        self.img_refresh = None
        self.subjects = []
        self.frame = frame
        self.controller = SubjectController()
        self.create_widgets()
        self.create_buttons()
        self.load_subject()

    def create_widgets(self):
        columns = ('subject_id', 'subject_name', 'subject_credit',
                   'subject_lesson', 'subject_category')
        self.tbl_subject = ttk.Treeview(self.frame, columns=columns,
                                        show='headings', height=10)
        self.tbl_subject.grid(row=0, column=0, columnspan=3,
                              sticky=tk.NSEW, pady=4, padx=4)
        set_style(self.tbl_subject)
        # show heading
        self.tbl_subject.heading('subject_id', text='Mã môn học')
        self.tbl_subject.heading('subject_name', text='Tên môn học')
        self.tbl_subject.heading('subject_credit', text='Số tín chỉ')
        self.tbl_subject.heading('subject_lesson', text='Số tiết học')
        self.tbl_subject.heading('subject_category', text='Loại môn học')
        # config columns
        self.tbl_subject.column(0, stretch=tk.NO, width=220, anchor=tk.CENTER)
        self.tbl_subject.column(1, stretch=tk.NO, width=220, anchor=tk.W)
        self.tbl_subject.column(2, stretch=tk.NO, width=220, anchor=tk.CENTER)
        self.tbl_subject.column(3, stretch=tk.NO, width=220, anchor=tk.CENTER)
        self.tbl_subject.column(4, stretch=tk.NO, width=220, anchor=tk.W)
        # add scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL,
                                  command=self.tbl_subject.yview)
        scrollbar.grid(row=0, column=3, sticky=tk.NS)
        self.tbl_subject['yscrollcommand'] = scrollbar.set
        # add buttons
        self.create_search_frame()
        self.create_sort_frame()

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
        ttk.Combobox(frm_search, values=search_subject_criterias,
                     textvariable=self.search_var). \
            grid(row=1, column=0, padx=16, pady=4, sticky=tk.W,
                 ipady=4, ipadx=16)
        # add search part
        ttk.Label(frm_search, text='Từ khóa:'). \
            grid(row=0, column=1, sticky=tk.W, padx=16, pady=4)
        self.search_entry = ttk.Entry(frm_search)
        self.search_entry.grid(row=1, column=1, sticky=tk.EW, padx=4, pady=4,
                               ipadx=16, ipady=4)
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
        ttk.Radiobutton(frm_sort, text='Theo mã môn học a-z', value=1,
                        variable=self.sort_var,
                        command=self.item_sort_by_id_selected). \
            grid(row=0, column=0, pady=4, padx=4, sticky=tk.W)
        ttk.Radiobutton(frm_sort, text='Theo tên môn học a-z',
                        value=2, variable=self.sort_var,
                        command=self.item_sort_by_name_selected). \
            grid(row=1, column=0, pady=4, padx=4, sticky=tk.W)
        ttk.Radiobutton(frm_sort, text='Theo số tín chỉ giảm dần',
                        value=3, variable=self.sort_var,
                        command=self.item_sort_by_credit_selected). \
            grid(row=0, column=1, pady=4, padx=4, sticky=tk.W)
        ttk.Radiobutton(frm_sort, text='Theo số tiết học tăng dần',
                        value=4, variable=self.sort_var,
                        command=self.item_sort_by_lesson_selected). \
            grid(row=1, column=1, pady=4, padx=4, sticky=tk.W)
        ttk.Radiobutton(frm_sort, text='Theo loại môn học a-z',
                        value=5, variable=self.sort_var,
                        command=self.item_sort_by_category_selected). \
            grid(row=2, column=0, pady=4, padx=4, sticky=tk.W)

    def create_buttons(self):
        button_frame = ttk.LabelFrame(self.frame, text='Các thao tác')
        button_frame.columnconfigure(0, weight=1, uniform='fred')
        button_frame.columnconfigure(1, weight=1, uniform='fred')
        button_frame.columnconfigure(2, weight=1, uniform='fred')
        button_frame.grid(row=2, column=0, columnspan=2,
                          padx=16, pady=4, sticky=tk.NSEW)
        self.img_refresh = tk.PhotoImage(file='view/assets/refresh.png')
        self.btn_reload = ttk.Button(button_frame, text='Làm mới', width=20,
                                     command=self.load_subject, image=self.img_refresh,
                                     compound=tk.LEFT)
        self.btn_reload.grid(row=0, column=0, ipady=4, ipadx=16, pady=4, padx=4)
        self.img_edit = tk.PhotoImage(file='view/assets/editing.png')
        self.btn_edit = ttk.Button(button_frame, text='Sửa môn học', width=20,
                                   command=self.btn_edit_subject_clicked,
                                   image=self.img_edit, compound=tk.LEFT)
        self.btn_edit.grid(row=0, column=1, ipady=4, ipadx=4, pady=4, padx=16)
        self.img_remove = tk.PhotoImage(file='view/assets/remove.png')
        self.btn_remove = ttk.Button(button_frame, text='Xóa bỏ', width=20,
                                     command=self.btn_remove_subject_clicked,
                                     image=self.img_remove, compound=tk.LEFT)
        self.btn_remove.grid(row=0, column=2, ipadx=4, ipady=4, pady=4, padx=16)

    def load_subject(self, should_show=True):
        self.subjects.clear()
        self.subjects = self.controller.read_file(SUBJECT_FILE_NAME)
        if should_show:
            self.show_subjects()

    def show_subjects(self):
        clear_treeview(self.tbl_subject)
        index = 1
        self.tbl_subject.selection_clear()
        for subject in self.subjects:
            if index % 2 == 0:
                tag = 'even'
            else:
                tag = 'odd'
            self.tbl_subject.insert('', tk.END,
                                    values=subject_to_tuple(subject),
                                    tags=(tag,), iid=f'{index - 1}')
            index += 1

    def btn_remove_subject_clicked(self):
        subjects = self.controller.read_file(SUBJECT_FILE_NAME)
        item_selected = self.tbl_subject.selection()
        if len(item_selected) > 0:
            title = 'Confirmation'
            message = 'Do you want to delete item(s) selected?'
            ans = askyesno(title, message)
            if ans:
                index = int(item_selected[0])
                subject_id = self.subjects[index].subject_id
                self.controller.remove(self.subjects, subject_id)  # xóa phần tử trong danh sách sinh viên
                self.controller.remove(subjects, subject_id)  # xóa phần tử trong danh sách nguyên bản
                self.tbl_subject.delete(item_selected[0])  # xóa phần tử trong bảng
                self.controller.write_file(SUBJECT_FILE_NAME, subjects)  # update file
                showinfo(title='Infomation', message=f'Delete subject id "{subject_id}" successfully!')
        else:
            showerror(title='Error', message='Please select a subject to delete first!')

    def btn_edit_subject_clicked(self):
        item_selected = self.tbl_subject.selection()
        if len(item_selected) > 0:
            index = int(item_selected[0])  # convert iid from str to int
            EditSubjectView(self, self.subjects[index]).attributes('-topmost', True)
        else:
            showerror(title='Error', message='Please select a subject to edit first!')
        pass

    def create_subject(self, subject: Subject):
        self.subjects.append(subject)
        self.show_subjects()

    def item_save_selected(self):
        self.controller.write_file(SUBJECT_FILE_NAME, self.subjects)

    def btn_search_clicked(self):
        key = self.search_entry.get()
        criteria = self.search_var.get()
        if len(key) == 0:
            showerror('Invalid keyword', 'Please enter keyword first!')
        elif len(criteria) == 0:
            showerror('Invalid criteria', 'Please select criteria to search!')
        else:
            if criteria == search_subject_criterias[0]:
                self.find_by_id(int(key))
            elif criteria == search_subject_criterias[1]:
                self.find_by_name(key)
            elif criteria == search_subject_criterias[2]:
                if is_credit_valid(key):
                    self.find_by_credit(int(key))
                else:
                    showerror('Invalid credit', 'Credit must be integer number from 2 to 15')
            elif criteria == search_subject_criterias[3]:
                if is_date_valid(key):
                    lesson = int(key)
                    self.find_by_lesson(lesson)
                else:
                    showerror('Invalid lesson', 'Lesson must be integer number from 1 to 54')
            elif criteria == search_subject_criterias[4]:
                self.find_by_category(key)

    def item_sort_by_id_selected(self):
        self.controller.sort_by_subject_id(self.subjects)
        self.show_subjects()

    def item_sort_by_name_selected(self):
        self.controller.sort_by_subject_name(self.subjects)
        self.show_subjects()

    def item_sort_by_credit_selected(self):
        self.controller.sort_by_subject_credit(self.subjects)
        self.show_subjects()

    def item_sort_by_lesson_selected(self):
        self.controller.sort_by_subject_lesson(self.subjects)
        self.show_subjects()

    def item_sort_by_category_selected(self):
        self.controller.sort_by_subject_category(self.subjects)
        self.show_subjects()

    def find_by_name(self, key: str):
        self.load_subject(False)  # reload subject
        result = self.controller.find_by_subject_name(self.subjects, key)
        self.check_result(result)

    def find_by_credit(self, key: int):
        self.load_subject(False)  # reload subject
        result = self.controller.find_by_subject_credit(self.subjects, key)
        self.check_result(result)

    def find_by_lesson(self, key: int):
        self.load_subject(False)  # reload subject
        result = self.controller.find_by_subject_lesson(self.subjects, key)
        self.check_result(result)

    def find_by_category(self, key: str):
        self.load_subject(False)  # reload subject
        result = self.controller.find_by_subject_category(self.subjects, key)
        self.check_result(result)

    def find_by_id(self, key: int):
        self.load_subject(False)  # reload subject
        result = self.controller.find_by_subject_id(self.subjects, key)
        if result is None:
            self.check_result([])
        else:
            self.check_result([result])

    def check_result(self, result: list[Subject]):
        if len(result) == 0:
            self.subjects.clear()
            self.show_subjects()
            showinfo('Search Result', 'No result found!')
        else:
            self.subjects.clear()
            self.subjects = result.copy()
            self.show_subjects()


class EditSubjectView(tk.Tk):
    def __init__(self, master, subject):
        super(EditSubjectView, self).__init__()
        self.columnconfigure(0, weight=1, uniform='fred')
        self.columnconfigure(1, weight=1, uniform='fred')
        self.btn_save = None
        self.btn_cancel = None
        self.entry_lesson = None
        self.entry_name = None
        self.entry_id = None
        self.combo_category = None
        self.combo_credit = None
        self.master = master
        self.subject = subject
        self.resizable(False, False)
        self.title('Edit Subject Information')
        self.create_widgets()
        self.setup_values()

    def create_widgets(self):
        self.entry_id = ttk.Entry(self, width=20)
        self.entry_name = ttk.Entry(self, width=20)
        self.entry_lesson = ttk.Entry(self, width=20)
        self.combo_credit = ttk.Combobox(self,
                                         values=credit_options(), width=17)
        self.combo_category = ttk.Combobox(self,
                                           values=subject_categories, width=17)
        # add button
        self.btn_cancel = ttk.Button(self, text='Cancel', width=20,
                                     command=self.destroy)
        self.btn_save = ttk.Button(self, text='Save', width=20,
                                   command=lambda: self.btn_save_clicked())
        # add label
        ttk.Label(self, text='Mã môn học:'). \
            grid(row=0, column=0, padx=16, pady=4, sticky=tk.W)
        ttk.Label(self, text='Tên môn học:'). \
            grid(row=1, column=0, padx=16, pady=4, sticky=tk.W)
        ttk.Label(self, text='Số tiết học:'). \
            grid(row=2, column=0, padx=16, pady=4, sticky=tk.W)
        ttk.Label(self, text='Số tín chỉ:'). \
            grid(row=3, column=0, padx=16, pady=4, sticky=tk.W)
        ttk.Label(self, text='Loại môn học:'). \
            grid(row=4, column=0, padx=16, pady=4, sticky=tk.W)
        # put into grid
        self.entry_id.grid(row=0, column=1, pady=4, padx=16)
        self.entry_name.grid(row=1, column=1, pady=4, padx=16)
        self.entry_lesson.grid(row=2, column=1, pady=4, padx=16)
        self.combo_credit.grid(row=3, column=1, pady=4, padx=16)
        self.combo_category.grid(row=4, column=1, pady=4, padx=16)
        self.btn_save.grid(row=5, column=1, pady=4, padx=16)
        self.btn_cancel.grid(row=5, column=0, pady=4, padx=16)

    def setup_values(self):
        self.entry_id.insert(0, str(self.subject.subject_id))
        self.entry_name.insert(0, self.subject.subject_name)
        self.entry_lesson.insert(0, str(self.subject.subject_lesson))
        # set value for combobox
        # first, find the index of item in the combobox
        credit_index = find_credit_index(self.subject.subject_credit)
        category_index = find_category_index(self.subject.subject_category)
        # then set that position into current function
        self.combo_credit.current(credit_index)
        self.combo_category.current(category_index)
        # disable entry with id -> deny change the id
        self.entry_id.configure(state='disabled')

    def btn_save_clicked(self):
        controller = SubjectController()
        ans = askyesno('Confirmation', 'Bạn có chắc muốn lưu các thay đổi?')
        if ans:
            try:
                subjects = controller.read_file(SUBJECT_FILE_NAME)
                name = self.entry_name.get()
                credit = int(self.combo_credit.get())
                lesson = int(self.entry_lesson.get())
                category = self.combo_category.get()
                controller.edit_subject(self.subject, name, credit, lesson, category)
                index = find_subject_index_by_id(subjects, self.subject.subject_id)
                controller.edit_subject(subjects[index], name, credit, lesson, category)
                controller.write_file(SUBJECT_FILE_NAME, subjects)
                self.master.show_subjects()
                showinfo('Completion', message='Update subject successfully!')
                self.destroy()
            except SubjectLessonError as e:
                showerror('SubjectLessonError', message=e.__str__())
                self.destroy()
            except SubjectCreditError as e:
                showerror('SubjectCreditError', message=e.__str__())
                self.destroy()


class AddNewSubjectView(tk.Tk):
    def __init__(self, master):
        super(AddNewSubjectView, self).__init__()
        self.columnconfigure(0, weight=1, uniform='fred')
        self.columnconfigure(1, weight=1, uniform='fred')
        self.btn_save = None
        self.btn_cancel = None
        self.entry_lesson = None
        self.entry_name = None
        self.entry_id = None
        self.combo_category = None
        self.combo_credit = None
        self.master = master
        self.resizable(False, False)
        self.title('Add New Subject')
        self.create_widgets()

    def create_widgets(self):
        self.entry_id = ttk.Entry(self, width=20)
        self.entry_id.configure(state='disabled')
        self.entry_name = ttk.Entry(self, width=20)
        self.entry_lesson = ttk.Entry(self, width=20)
        self.combo_credit = ttk.Combobox(self,
                                         values=credit_options(), width=17)
        self.combo_category = ttk.Combobox(self,
                                           values=subject_categories, width=17)
        # add button
        self.btn_cancel = ttk.Button(self, text='Cancel', width=20,
                                     command=self.destroy)
        self.btn_save = ttk.Button(self, text='Create', width=20,
                                   command=lambda: self.btn_add_clicked())
        # add label
        ttk.Label(self, text='Mã môn học:'). \
            grid(row=0, column=0, padx=16, pady=4, sticky=tk.W)
        ttk.Label(self, text='Tên môn học:'). \
            grid(row=1, column=0, padx=16, pady=4, sticky=tk.W)
        ttk.Label(self, text='Số tiết học:'). \
            grid(row=2, column=0, padx=16, pady=4, sticky=tk.W)
        ttk.Label(self, text='Số tín chỉ:'). \
            grid(row=3, column=0, padx=16, pady=4, sticky=tk.W)
        ttk.Label(self, text='Loại môn học:'). \
            grid(row=4, column=0, padx=16, pady=4, sticky=tk.W)
        # put into grid
        self.entry_id.grid(row=0, column=1, pady=4, padx=16)
        self.entry_name.grid(row=1, column=1, pady=4, padx=16)
        self.entry_lesson.grid(row=2, column=1, pady=4, padx=16)
        self.combo_credit.grid(row=3, column=1, pady=4, padx=16)
        self.combo_category.grid(row=4, column=1, pady=4, padx=16)
        self.btn_save.grid(row=5, column=1, pady=4, padx=16)
        self.btn_cancel.grid(row=5, column=0, pady=4, padx=16)

    def btn_add_clicked(self):
        controller = SubjectController()
        try:
            name = self.entry_name.get()
            credit = int(self.combo_credit.get())
            lesson = int(self.entry_lesson.get())
            category = self.combo_category.get()
            subject = controller.create_subject(0, name, credit, lesson, category)
            self.master.create_subject(subject=subject)
            showinfo('Action Success', message='Add new subject successfully!')
            self.destroy()
        except SubjectLessonError as e:
            showerror('SubjectLessonError', message=e.__str__())
            self.destroy()
        except SubjectCreditError as e:
            showerror('SubjectCreditError', message=e.__str__())
            self.destroy()