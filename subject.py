class Subject:
    AUTO_ID = 1000

    def __init__(self, subject_id, name, credit, lesson, category):
        if subject_id != 0:
            self.__subject_id = subject_id
        else:
            self.__subject_id = Subject.AUTO_ID
            Subject.AUTO_ID += 1
        self.__name = name
        self.__credit = credit
        self.__lesson = lesson
        self.__category = category

    @property
    def subject_id(self):
        return self.__subject_id

    @subject_id.setter
    def subject_id(self, value):
        self.__subject_id = value

    @property
    def subject_name(self):
        return self.__name

    @subject_name.setter
    def subject_name(self, value):
        self.__name = value

    @property
    def subject_credit(self):
        return self.__credit

    @subject_credit.setter
    def subject_credit(self, value):
        self.__credit = value

    @property
    def subject_category(self):
        return self.__category

    @subject_category.setter
    def subject_category(self, value):
        self.__category = value

    @property
    def subject_lesson(self):
        return self.__lesson

    @subject_lesson.setter
    def subject_lesson(self, value):
        self.__lesson = value

    def to_dict(self):
        return {
            "subject_id": self.subject_id,
            "subject_name": self.subject_name,
            "subject_credit": self.subject_credit,
            "subject_lesson": self.subject_lesson,
            "subject_category": self.subject_category
        }