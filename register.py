class Register:
    AUTO_ID = 1000

    def __init__(self, reg_id=0, student=None, subject=None, reg_time=None):
        if reg_id != 0:
            self.__register_id = reg_id
        else:
            self.__register_id = Register.AUTO_ID
            Register.AUTO_ID += 1
        self.__student = student
        self.__subject = subject
        self.__register_time = reg_time

    @property
    def register_id(self):
        return self.__register_id

    @register_id.setter
    def register_id(self, value):
        self.__register_id = value

    @property
    def student(self):
        return self.__student

    @student.setter
    def student(self, value):
        self.__student = value

    @property
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self, value):
        self.__subject = value

    @property
    def register_time(self):
        return self.__register_time

    @register_time.setter
    def register_time(self, value):
        self.__register_time = value

    def to_dict(self):
        return {
            "reg_id": self.register_id,
            "subject_id": self.subject.subject_id,
            "student_id": self.student.student_id,
            "reg_time": self.register_time.strftime('%d/%m/%Y %H:%M:%S')
        }