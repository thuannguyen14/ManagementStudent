import tkinter
from tkinter import ttk
from tkinter.messagebox import showinfo, askyesno, showerror

from controller.studentcontroller import StudentController
from error.exceptions import GpaError
from utils import STUDENT_FILE_NAME, find_student_index_by_id


class EditStudentView(tkinter.Tk):
    def __init__(self, master, student):
        super(EditStudentView, self).__init__()
        self.btn_save = None
        self.btn_cancel = None
        self.entry_gpa = None
        self.entry_full_name = None
        self.entry_student_id = None
        self.master = master
        self.student = student
        self.resizable(False, False)
        self.title('Edit GPA')
        self.create_widgets()

    def create_widgets(self):
        self.entry_student_id = ttk.Entry(self)
        self.entry_full_name = ttk.Entry(self)
        self.entry_gpa = ttk.Entry(self)
        # insert text
        self.entry_student_id.insert(0, str(self.student.student_id))
        self.entry_full_name.insert(0, str(self.student.full_name))
        self.entry_gpa.insert(0, str(self.student.gpa))
        # disable all entry but gpa entry
        self.entry_full_name.configure(state='disabled')
        self.entry_student_id.configure(state='disabled')
        # add button
        self.btn_cancel = ttk.Button(self, text='Cancel', command=self.destroy)
        self.btn_save = ttk.Button(self, text='Save', command=lambda: self.check_error())
        # add label
        ttk.Label(self, text='Mã SV:').grid(row=0, column=0, padx=4, pady=2)
        ttk.Label(self, text='Họ và tên:').grid(row=1, column=0, padx=4, pady=2)
        ttk.Label(self, text='Điểm TB:').grid(row=2, column=0, padx=4, pady=2)
        # put into grid
        self.entry_student_id.grid(row=0, column=1, pady=2, padx=4)
        self.entry_full_name.grid(row=1, column=1, pady=2, padx=4)
        self.entry_gpa.grid(row=2, column=1, pady=2, padx=4)
        self.btn_save.grid(row=3, column=1, pady=4, padx=4)
        self.btn_cancel.grid(row=3, column=0, pady=4, padx=4)

    def check_error(self):
        controller = StudentController()
        gpa = float(self.entry_gpa.get())
        ans = askyesno('Confirmation', 'Bạn có chắc muốn lưu các thay đổi?')
        if ans:
            try:
                students = controller.read_file(STUDENT_FILE_NAME)
                controller.update_gpa(student=self.student, gpa=gpa)
                index = find_student_index_by_id(students, self.student.student_id)
                controller.update_gpa(students[index], gpa)
                controller.write_file(STUDENT_FILE_NAME, students)
                self.master.show_students()
                showinfo('Completion', message='Update student\'s GPA successfully!')
                self.destroy()
            except GpaError as e:
                showerror('GPA Error', message=e.__str__())
                self.destroy()