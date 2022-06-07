import random
from django.utils import timezone

class Percentage:
    def __init__(self, value, total):
        self.value = value
        self.total = total
        self.percentage = round((self.value / self.total * 100), 1)


class Attendance_code:
    list = []

    def __init__(self, event):
        self.event = event
        code = random.randrange(0, 1000)
        temp_list = [c.code for c in Attendance_code.list]
        while code in temp_list:
            code = random.randrange(0, 1000)

        self.code = code
        self.expired_date = timezone.now() + timezone.timedelta(minutes=10)
        Attendance_code.list.append(self)

    @staticmethod
    def get_code(event):
        for atd in Attendance_code.list:
            if atd.event == event:
                if timezone.now() < atd.expired_date:
                    return atd.code
                else:
                    return None
        return None

    @staticmethod
    def check(code):
        for atd in Attendance_code.list:
            if atd.code == code:
                if timezone.now() < atd.expired_date:
                    return atd.event
        return None
