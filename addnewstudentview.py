import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
from utils import majors
from controller.studentcontroller import StudentController


class AddNewStudentView(tk.Tk):
    def __init__(self, master):
        super(AddNewStudentView, self).__init__()
        self.btn_add = None
        self.btn_cancel = None
        self.combo_major = None
        self.entry_birth_date = None
        self.entry_gpa = None
        self.entry_address = None
        self.entry_email = None
        self.entry_full_name = None
        self.entry_person_id = None
        self.master = master
        # self.geometry('300x220')
        self.resizable(False, False)
        self.columnconfigure(0, weight=1, uniform='fred')
        self.columnconfigure(1, weight=1, uniform='fred')
        self.title('Add New Student Window')
        self.create_widgets()

    def create_widgets(self):
        self.entry_person_id = ttk.Entry(self, width=25)
        self.entry_full_name = ttk.Entry(self, width=25)
        self.entry_email = ttk.Entry(self, width=25)
        self.entry_address = ttk.Entry(self, width=25)
        self.entry_address.insert(0, 'Phường, Quận, Thành phố')
        self.entry_gpa = ttk.Entry(self, width=25)
        self.entry_birth_date = ttk.Entry(self, width=25)
        self.combo_major = ttk.Combobox(self, values=majors)
        # add button
        self.btn_cancel = ttk.Button(self, text='Cancel', width=20,
                                     command=self.destroy)
        self.btn_add = ttk.Button(self, text='Add', width=20,
                                  command=lambda: self.check_error())
        # add label
        ttk.Label(self, text='CMND/CCCD:').grid(row=0, column=0, padx=8, pady=4, sticky=tk.W)
        ttk.Label(self, text='Họ và tên:').grid(row=1, column=0, padx=8, pady=4, sticky=tk.W)
        ttk.Label(self, text='Ngày sinh:').grid(row=2, column=0, padx=8, pady=4, sticky=tk.W)
        ttk.Label(self, text='Email:').grid(row=3, column=0, padx=8, pady=4, sticky=tk.W)
        ttk.Label(self, text='Địa chỉ:').grid(row=4, column=0, padx=8, pady=4, sticky=tk.W)
        ttk.Label(self, text='Điểm TB:').grid(row=5, column=0, padx=8, pady=4, sticky=tk.W)
        ttk.Label(self, text='Chuyên ngành:').grid(row=6, column=0, padx=8, pady=4, sticky=tk.W)
        # put into grid
        self.entry_person_id.grid(row=0, column=1, pady=4, padx=8, sticky=tk.EW)
        self.entry_full_name.grid(row=1, column=1, pady=4, padx=8)
        self.entry_birth_date.grid(row=2, column=1, pady=4, padx=8)
        self.entry_email.grid(row=3, column=1, pady=4, padx=8)
        self.entry_address.grid(row=4, column=1, padx=8, pady=4)
        self.entry_gpa.grid(row=5, column=1, pady=4, padx=8)
        self.combo_major.grid(row=6, column=1, pady=4, padx=8, sticky=tk.EW)
        self.btn_add.grid(row=7, column=1, pady=4, padx=8)
        self.btn_cancel.grid(row=7, column=0, pady=4, padx=8)

    def check_error(self):
        controller = StudentController()
        person_id = self.entry_person_id.get()
        fname = self.entry_full_name.get()
        dob = self.entry_birth_date.get()
        email = self.entry_email.get()
        addr = self.entry_address.get()
        gpa_str = self.entry_gpa.get()
        major = self.combo_major.get()
        if len(major) == 0:
            showerror('Major invalid', 'Please select a major to continue.')
        else:
            student = controller.add(person_id, fname, dob, email, addr, gpa_str, major)
            if student is not None:
                self.master.item_create_student_selected(student)
                showinfo('Completion', message='Add new student successfully!')