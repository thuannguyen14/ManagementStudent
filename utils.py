import re
from datetime import datetime
from tkinter.ttk import Treeview
from tkinter import ttk

from model.register import Register
from model.student import Student, BirthDate, FullName, Address
from model.subject import Subject

STUDENT_FILE_NAME = 'student.json'
SUBJECT_FILE_NAME = 'subject.json'
REGISTER_FILE_NAME = 'register.json'

search_student_criterias = [
    'Tìm theo tên',
    'Tìm theo điểm TB',
    'Tìm theo ngày sinh',
    'Tìm theo tháng sinh',
    'Tìm theo năm sinh'
]

search_subject_criterias = [
    'Tìm theo mã môn học',
    'Tìm theo tên gần đúng',
    'Tìm theo số tín chỉ',
    'Tìm theo số tiết học',
    'Tìm theo loại môn học'
]

capacities = [
    'Xuất sắc',
    'Giỏi',
    'Khá',
    'Trung bình',
    'Yếu'
]

majors = [
    'Công nghệ thông tin',
    'Công nghệ sinh học',
    'Đa phương tiện',
    'Quản trị kinh doanh',
    'Điện tử viễn thông',
    'Quản trị nhân lực'
]

subject_categories = [
    'Cơ sở ngành',
    'Chuyên ngành',
    'Tự chọn',
    'Cơ bản',
    'Nâng cao'
]

search_register_criterias = [
    'Tìm theo mã sinh viên',
    'Tìm theo mã môn học'
]


def set_style(tbl: Treeview, theme: str = 'default'):
    style = ttk.Style()
    style.theme_use(theme)  # other theme can use: clam, classic, default
    style.configure('my.Treeview.Heading', font=('Calibri', 11, 'bold'),
                    background='#6caf50', foreground='#ffffff')
    tbl.configure(style='my.Treeview')
    # customize style for odd and even row background color
    tbl.tag_configure('odd', background='#f0f0f0')
    tbl.tag_configure('even', background='#ffffff')


def credit_options() -> []:
    values = []
    for i in range(15):
        values.append(i + 1)
    return values


def find_credit_index(credit: int) -> int:
    credits_ = credit_options()
    for c in credits_:
        if c == credit:
            return c - 1
    return -1


def find_subject_index_by_id(subjects: list[Subject], subject_id: int) -> int:
    index = 0
    for sub in subjects:
        if sub.subject_id == subject_id:
            return index
        index += 1
    return -1


def find_category_index(category: str) -> int:
    index = 0
    for cate in subject_categories:
        if cate == category:
            return index
        index += 1
    return -1


def is_gpa_valid(gpa_str: str) -> bool:
    pattern = r'^(\d+.\d+)|\d+|.\d+$'
    pattern2 = r'.*\s+.*'
    if re.match(pattern, gpa_str.strip()) and not re.match(pattern2, gpa_str.strip()):
        return True
    else:
        return False


def is_credit_valid(credit: str) -> bool:
    pattern = '.*[^0-9\\s].*'
    matcher = re.search(pattern, credit)
    if matcher:
        return False
    else:
        int_value = int(credit)
        if int_value < 2 or int_value > 15:
            return False
        return True


def is_student_id_valid(student_id: str):
    pattern = r'SV[1-9]{1}\d{3}'
    matcher = re.search(pattern, student_id, flags=re.IGNORECASE)
    if matcher:
        return True
    else:
        return False


def is_subject_id_valid(subject_id: str):
    pattern = r'\d{4}'
    matcher = re.search(pattern, subject_id)
    if matcher:
        return True
    else:
        return False


def is_date_valid(input_str: str) -> bool:
    pattern = r'\d+'
    if re.search(pattern, input_str):
        return True
    else:
        return False


def capacity(gpa: float) -> str:
    if gpa >= 3.6:
        return 'Xuất sắc'
    elif gpa >= 3.2:
        return 'Giỏi'
    elif gpa >= 2.6:
        return 'Khá'
    elif gpa >= 2.0:
        return 'Trung bình'
    else:
        return 'Yếu'


def get_subject_id(subjects: list[Subject]) -> list[str, ...]:
    result = []
    for subject in subjects:
        result.append(f'{subject.subject_id}')
    return result


def student_to_tuple(student: Student) -> tuple[str, ...]:
    """ Hàm tiện ích thực hiện chuyển đổi thông tin sinh viên thành một
        tuple chứa các phần tử biểu diễn ở string.
    """
    return tuple([student.person_id, student.full_name,
                  student.birth_date, student.student_id,
                  student.email, student.address,
                  f'{student.gpa:0.2f}', student.major])


def subject_to_tuple(subject: Subject) -> tuple[str, ...]:
    return tuple([subject.subject_id, subject.subject_name,
                  subject.subject_credit, subject.subject_lesson,
                  subject.subject_category])


def register_to_tuple(register: Register) -> tuple[str, ...]:
    return tuple([register.register_id, register.subject.subject_id,
                  register.subject.subject_name, register.student.student_id,
                  register.student.full_name,
                  datetime.strftime(register.register_time, '%d/%m/%Y %H:%M:%S')])


def clear_treeview(treeview):
    """ Hàm tiện ích dùng để xóa toàn bộ bản ghi trong bảng(treeview)
        trước khi hiển thị thông tin mới vào đó nhằm tránh trùng lặp các bản ghi.
    """
    for item in treeview.get_children():
        treeview.delete(item)


def create_birth_date(data: str) -> BirthDate:
    items = data.split('/')
    day, month, year = int(items[0]), items[1], items[2]
    return BirthDate(day, month, year)


def decode_full_name(dct):
    if 'first' in dct:
        return FullName(dct['first'], dct['last'], dct['mid'])
    else:
        return dct


def decode_address(dct):
    if 'city' in dct:
        return Address(dct['wards'], dct['district'], dct['city'])
    return dct


def decode_birth_date(dct):
    if 'day' in dct:
        return BirthDate(int(dct['day']), int(dct['month']), int(dct['year']))
    return dct


def decode_student(dct):
    if 'student_id' in dct:
        pid = dct['person_id']
        full_name = decode_full_name(dct['full_name'])
        birth_date = decode_birth_date(dct['birth_date'])
        address = decode_address(dct['address'])
        sid = dct['student_id']
        email = dct['email']
        major = dct['major']
        gpa = float(dct['gpa'])
        return Student(pid, full_name, birth_date, sid, email, address, gpa, major)
    else:
        return dct


def decode_register(dct):
    if 'reg_id' in dct:
        reg_id = int(dct['reg_id'])
        subject_id = int(dct['subject_id'])
        student_id = dct['student_id']
        reg_time = datetime.strptime(dct['reg_time'], '%d/%m/%Y %H:%M:%S')
        return Register(reg_id, student_id, subject_id, reg_time)
    else:
        return dct


def delta_time(tm):
    birth_date = datetime.strptime(tm.__str__(), '%d/%m/%Y')
    total_sec = (birth_date - datetime.strptime('01/01/1970', '%d/%m/%Y')).total_seconds()
    return total_sec


def register_delta_time(tm):
    return (tm - datetime.strptime('01/01/1970', '%d/%m/%Y')).total_seconds()


def create_full_name(fname: str) -> FullName:
    data = fname.split(' ')
    first_name = data[len(data) - 1]
    last_name = data[0]
    mid_name = ''
    for i in range(1, len(data) - 1):
        mid_name += data[i]
    return FullName(first_name, last_name, mid_name.strip())


def create_address(address: str) -> Address:
    data = address.split(', ')
    wards = data[0]
    district = data[1]
    city = data[2]
    return Address(wards, district, city)


def remove_student_from_list(students: list[Student], student_id: str) -> list[Student]:
    index = 0
    for student in students:
        if student.student_id == student_id:
            students.pop(index)
            break
        index += 1
    return students


def find_student_index_by_id(students: list[Student], student_id: str) -> int:
    for i in range(len(students)):
        if students[i].student_id == student_id:
            return i
    return -1


def decode_subject(dct):
    if 'subject_id' in dct:
        sid = int(dct['subject_id'])
        name = dct['subject_name']
        credit = int(dct['subject_credit'])
        lesson = int(dct['subject_lesson'])
        category = dct['subject_category']
        return Subject(sid, name, credit, lesson, category)
    else:
        return dct