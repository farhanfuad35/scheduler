# We need to know if teacher i is available on day d at slot s. bool teacher[i][d][s]

import datetime
import django_excel as excel

SLOTS_PER_DAY = []

class Teacher:
    def __init__(self, initial, teacher_slots):
        self.initial = initial
        self.days = []
        for i in range(0, 5):
            slots = []

            for t in SLOTS_PER_DAY:
                available = False
                for s in teacher_slots[i]:
                    if t >= s[0] and t <= s[1]:
                        available = True
                        break
                slots.append(available)

            self.days.append(slots)
        
        # for i in range(0, 5):
        #     print(i, ' ---------- ', len(self.days[i]))
        #     for item in self.days[i]:
        #         print(item)


def schedule(book):
    global SLOTS_PER_DAY
    SLOTS_PER_DAY = [
            datetime.datetime.strptime('08:30 AM', '%I:%M %p'),
            datetime.datetime.strptime('10:00 AM', '%I:%M %p'),
            datetime.datetime.strptime('11:30 AM', '%I:%M %p'),
            datetime.datetime.strptime('02:00 PM', '%I:%M %p'),
            datetime.datetime.strptime('03:30 PM', '%I:%M %p')
        ]

    teachers = preProcess(book)


def preProcess(book):
    timetable = book['Sheet3'].get_array()
    timetable.pop(0)
    teachers = []
    for rec in timetable:
        initial = rec[0]
        teacher_slots = []
        teacher_slots.append(convertToTime(rec[2]))
        teacher_slots.append(convertToTime(rec[3]))
        teacher_slots.append(convertToTime(rec[4]))
        teacher_slots.append(convertToTime(rec[5]))
        teacher_slots.append(convertToTime(rec[6]))

        teachers.append(Teacher(initial, teacher_slots))

def convertToTime(str):
    timeStrArr = str.split(';')
    ret = []
    for t in timeStrArr:
        try:
            startTime = t.split('-')[0]
            startTime = datetime.datetime.strptime(startTime, '%I:%M%p')
            endTime = t.split('-')[1]
            endTime = datetime.datetime.strptime(endTime, '%I:%M%p')
            ret.append([startTime, endTime])
        except ValueError:
            return ret
    
    return ret