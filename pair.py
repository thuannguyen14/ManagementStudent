from model.subject import Subject


class Pair:
    def __init__(self, subject: Subject, num_of_register: int):
        self.subject = subject
        self.number_of_register = num_of_register