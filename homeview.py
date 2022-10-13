import tkinter as tk
from tkinter import ttk, Menu
from tkinter.messagebox import showinfo

from utils import set_style
from view.addnewstudentview import AddNewStudentView
from view.registerview import RegisterView
from view.studentview import StudentView
from view.subjectview import SubjectView, AddNewSubjectView


class HomeView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.notebook = None
        self.register_view = None
        self.subject_view = None
        self.student_view = None
        self.frm_register = None
        self.frm_subject = None
        self.frm_student = None
        self.title('QUẢN LÝ ĐĂNG KÝ MÔN HỌC')
        self.resizable(False, False)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.menubar = Menu()
        self.configure(menu=self.menubar)
        self.iconbitmap('./view/assets/Logo_Hust.png')
        self.create_notebook()
        self.create_child_views()
        self.create_menu()

    def create_notebook(self):
        self.notebook = ttk.Notebook()
        self.notebook.grid(row=0, column=0, sticky=tk.NSEW)
        # add student frame
        self.frm_student = ttk.Frame(self.notebook)
        # cấu hình cho các cột của frame có cùng độ rộng
        self.frm_student.columnconfigure(0, weight=1, uniform='fred')
        self.frm_student.columnconfigure(1, weight=1, uniform='fred')
        self.frm_student.columnconfigure(2, weight=1, uniform='fred')
        self.frm_student.grid(row=0, column=0)
        # add subject frame
        self.frm_subject = ttk.Frame(self.notebook)
        self.frm_subject.columnconfigure(0, weight=1, uniform='fred')
        self.frm_subject.columnconfigure(1, weight=1, uniform='fred')
        self.frm_subject.grid(row=0, column=0)
        # add register frame
        self.frm_register = ttk.Frame(self.notebook)
        self.frm_register.columnconfigure(0, weight=1, uniform='fred')
        self.frm_register.columnconfigure(1, weight=1, uniform='fred')
        self.frm_register.columnconfigure(2, weight=1, uniform='fred')
        self.frm_register.grid(row=0, column=0)
        # add frame to self.notebook
        self.notebook.add(self.frm_student, text='Student Managerment')
        self.notebook.add(self.frm_subject, text='Subject Managerment')
        self.notebook.add(self.frm_register, text='Register Managerment')

    def create_menu(self):
        file_menu = Menu(self.menubar, tearoff=False)
        submenu_file = Menu(file_menu, tearoff=False)
        submenu_file.add_command(label='Student',
                                 command=lambda: self.create_student())
        submenu_file.add_command(label='Subject',
                                 command=lambda: self.create_subject())
        submenu_file.add_command(label='Register',
                                 command=lambda: self.create_register())
        file_menu.add_cascade(label='Create New...',
                              underline=0, menu=submenu_file)
        # save menu item
        file_menu.add_command(label='Save', command=lambda: self.save())
        # other menu items
        file_menu.add_separator()
        file_menu.add_command(label='Exit', underline=0, command=self.destroy)
        # add to menu bar
        self.menubar.add_cascade(label='File', menu=file_menu, underline=0)
        self.menubar.add_cascade(label='Help', underline=0)
        sub_menu_setting = Menu(tearoff=False)
        sub_menu_theme = Menu(tearoff=False)
        sub_menu_theme.add_command(label='Default', command=lambda: self.change_theme('default'))
        sub_menu_theme.add_command(label='Alt', command=lambda: self.change_theme('alt'))
        sub_menu_theme.add_command(label='Clam', command=lambda: self.change_theme('clam'))
        sub_menu_theme.add_command(label='Classic', command=lambda: self.change_theme('classic'))
        sub_menu_setting.add_cascade(label='Themes', menu=sub_menu_theme)
        self.menubar.add_cascade(label='Settings', menu=sub_menu_setting, underline=0)

    def create_child_views(self):
        self.student_view = StudentView(self.frm_student)
        self.subject_view = SubjectView(self.frm_subject)
        self.register_view = RegisterView(self.frm_register)

    def create_student(self):
        popup = AddNewStudentView(self.student_view)
        popup.attributes('-topmost', True)  # showing popup alway on top of master frame
        popup.mainloop()

    def save(self):
        self.student_view.item_save_selected()
        self.subject_view.item_save_selected()
        self.register_view.item_save_selected()
        showinfo('Successfully', 'Save data to file successfully!')

    def create_subject(self):
        popup = AddNewSubjectView(self.subject_view)
        popup.attributes('-topmost', True)
        popup.mainloop()

    def create_register(self):
        self.notebook.select(2)
        self.register_view.entry_student_id.focus()

    def change_theme(self, theme: str):
        set_style(self.register_view.tbl_register, theme)
        set_style(self.student_view.tbl_student, theme)
        set_style(self.subject_view.tbl_subject, theme)