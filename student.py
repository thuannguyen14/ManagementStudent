class FullName:
    def __init__(self, first, last, mid):
        self.__first = first
        self.__last = last
        self.__mid = mid

    @property
    def first_name(self):
        return self.__first

    @first_name.setter
    def first_name(self, value):
        self.__first = value

    @property
    def last_name(self):
        return self.__last

    @last_name.setter
    def last_name(self, value):
        self.__last = value

    @property
    def mid_name(self):
        return self.__mid

    @mid_name.setter
    def mid_name(self, value):
        self.__mid = value

    def __str__(self):
        return f'{self.last_name} {self.mid_name} {self.first_name}'


class Address:
    def __init__(self, wards, district, city):
        self.__wards = wards
        self.__district = district
        self.__city = city

    @property
    def wards(self):
        return self.__wards

    @property
    def district(self):
        return self.__district

    @property
    def city(self):
        return self.__city

    @wards.setter
    def wards(self, value):
        self.__wards = value

    @district.setter
    def district(self, value):
        self.__district = value

    @city.setter
    def city(self, value):
        self.__city = value

    def __str__(self):
        return f'{self.wards}, {self.district}, {self.city}'


class BirthDate:
    def __init__(self, day, month, year):
        self.__day = day
        self.__month = month
        self.__year = year

    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self, value):
        self.__day = value

    @property
    def month(self):
        return self.__month

    @month.setter
    def month(self, value):
        self.__month = value

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        self.__year = value

    def __str__(self):
        return f'{self.day}/{self.month}/{self.year}'


class Person:
    def __init__(self, person_id, full_name, birth_date, address):
        self.__person_id = person_id
        self.__full_name = full_name
        self.__birth_date = birth_date
        self.__address = address

    @property
    def person_id(self):
        return self.__person_id

    @property
    def full_name(self):
        return self.__full_name

    @property
    def birth_date(self):
        return self.__birth_date

    @person_id.setter
    def person_id(self, value):
        self.__person_id = value

    @full_name.setter
    def full_name(self, value):
        self.__full_name = value

    @birth_date.setter
    def birth_date(self, value):
        self.__birth_date = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value


class Student(Person):
    AUTO_ID = 1000

    def __init__(self, person_id, full_name,
                 birth_date, student_id, email, address, gpa, major):
        super().__init__(person_id, full_name, birth_date, address)
        if student_id is None:
            self.student_id = f'SV{Student.AUTO_ID}'
            Student.AUTO_ID += 1
        else:
            self.__student_id = student_id
        self.__email = email
        self.__gpa = gpa
        self.__major = major
        self.__capacity = ''

    @property
    def student_id(self):
        return self.__student_id

    @student_id.setter
    def student_id(self, value):
        self.__student_id = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def gpa(self):
        return self.__gpa

    @gpa.setter
    def gpa(self, value):
        self.__gpa = value

    @property
    def major(self):
        return self.__major

    @major.setter
    def major(self, value):
        self.__major = value

    @property
    def capacity(self):
        return self.__capacity

    @capacity.setter
    def capacity(self, value):
        self.__capacity = value

    def to_dict(self):
        return {
            'person_id': self.person_id,
            'full_name': {
                'first': self.full_name.first_name,
                'last': self.full_name.last_name,
                'mid': self.full_name.mid_name
            },
            'birth_date': {
                'day': self.birth_date.day,
                'month': self.birth_date.month,
                'year': self.birth_date.year
            },
            'address': {
                'wards': self.address.wards,
                'district': self.address.district,
                'city': self.address.city
            },
            'student_id': self.student_id,
            'email': self.email,
            'major': self.major,
            'gpa': self.gpa
        }