# We need to know if teacher i is available on day d at slot s. bool teachers[i].days[d][s]
# groupFree[302][1] = True : group 302 (Year 3, Semester 0, Section 2) is free (True) on Monday (1)

# In Teacher, courses[302] = 4 : courses 

import datetime
import django_excel as excel
from .algo import runAlgo

SLOTS_PER_DAY = []
NUMBER_OF_SLOTS = 5

batches = {}
teachers = {}
courses = {}

class Teacher:
    def __init__(self, initial, teacherSlots, courses):
        self.initial = initial
        self.available = True
        self.courses = courses          # These are all course keys, not actual course
        self.routine = []
        self.teacherSlots = teacherSlots              # An array containing an array of Times. teacherSlots[1][0] = startTime, [1][1] = endTime of the 2nd (1) slot

        for i in range(5):
            self.routine.append([None, None, None, None, None])

    def __str__(self):
        return self.initial

    # def __lt__(self, other):
    #     now = datetime.datetime.now()
    #     tm1 = now
    #     tm2 = now
    #     for day in self.teacherSlots:
    #         for slot in day:
    #             tm1 = tm1 + (slot[1]-slot[0])
    #     for day in other.teacherSlots:
    #         for slot in day:
    #             tm2 = tm2 + (slot[1]-slot[0])
        
    #     return tm1 < tm2


class Batch:
    def __init__(self, id):
        self.free = []                         # A 2D array. free[2][3] = free at Tuesday (2) at 2:00 PM (slot: 3)
        self.id = id
        self.available = True
        
        for j in range(0, 5):
            slots = []
            for i in range(0, NUMBER_OF_SLOTS):
                slots.append(True)
            self.free.append(slots)
        
class Course:
    def __init__(self, id, name, credit):
        self.id = id
        self.name = name
        self.credit = credit
        self.duration = 1.5
        self.doneClass = 0
        self.isLabCourse = False
        self.courseTeachers = []
        self.available = True

        if credit == 3:
            self.weeklyClass = 2
        elif credit == 1.5:
            self.weeklyClass = 1
        else:
            self.weeklyClass = 2

        if int(id/100)%10 == 1:
            self.isLabCourse = True
            self.weeklyClass = 1
            self.duration = 3


    def __str__(self):
        if self.isLabCourse:
            lab = 'Lab Course'
        else:
            lab = 'Not a lab course'
        return 'Course id: ' + str(self.id) + '\nCredit: ' + str(self.credit) + '\n' + lab + '\nWeekly Class: ' + str(self.weeklyClass)
        

def schedule(book):
    global SLOTS_PER_DAY
    global NUMBER_OF_SLOTS
    global teachers
    global courses

    NUMBER_OF_SLOTS = 5
    SLOTS_PER_DAY = (
            datetime.datetime.strptime('08:30 AM', '%I:%M %p'),
            datetime.datetime.strptime('10:00 AM', '%I:%M %p'),
            datetime.datetime.strptime('11:30 AM', '%I:%M %p'),
            datetime.datetime.strptime('02:00 PM', '%I:%M %p'),
            datetime.datetime.strptime('03:30 PM', '%I:%M %p')
        )

    preProcess(book)
    applyHeuristics()

    return runAlgo(batches, courses, teachers, SLOTS_PER_DAY, numberOfClasses())
    # Test
    # for key in batches.keys():
    #     print(batches[key].id)

    # print('----------------')

    # for teacher in teachers:
    #     print('-- New Teacher --')
    #     for course in teacher.courses:
    #         print(course)

    # for key in courses.keys():
    #     print(courses[key])

    # for key in courses.keys():
    #     print(courses[key].id)
    #     for teacher in courses[key].courseTeachers:
    #         print(teacher.initial)


# Convert excel to python objects

def preProcess(book):
    timetable = book[2].get_array()
    timetable.pop(0)
    global teachers
    for rec in timetable:
        initial = rec[0]
        teacherSlots = []
        teacherSlots.append(convertToTime(rec[2]))
        teacherSlots.append(convertToTime(rec[3]))
        teacherSlots.append(convertToTime(rec[4]))
        teacherSlots.append(convertToTime(rec[5]))
        teacherSlots.append(convertToTime(rec[6]))

        courses = getTeacherCourses(book, initial)
        teacher = Teacher(initial, teacherSlots, courses)

        setCourseTeacher(teacher)

        teachers[initial] = teacher

def setCourseTeacher(teacher):
    for course in teacher.courses:
        courses[course].courseTeachers.append(teacher)

def numberOfClasses():
    n=0
    for key in courses.keys():
        n = n + courses[key].weeklyClass
    return n

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

# Convert courses to id. CSE 3201 would be converted into 320 (3: Year, 2: Semester, 0: No Section)
# CSE 3102 Section 2 would be converted into 312 (3: Year, 1: Semester, 2: Section)

# This method also generates batch array and courses array while reading courses from the excel

def getTeacherCourses(book, initial):
    global batches
    global courses

    sheet = book[1].get_array()
    teacherCourses = []
    for row in sheet:
        if row[0] == initial:
            for i in range(1, len(row)):
                if row[i] != '':
                    splittedCourseName = row[i].split(' Section ')
                    
                    courseID = int(splittedCourseName[0][-4:])

                    batchID = int(courseID/100)
                    if len(splittedCourseName) > 1:
                        courseID = courseID *10 + int(splittedCourseName[1])
                        batchID = batchID*10 + int(splittedCourseName[1])
                    else:
                        courseID = courseID * 10
                        batchID = batchID * 10

                    teacherCourses.append(courseID)

                    # If you want to change course credit, do it here. Default is all 3
                    if courseID not in courses.keys():
                        courses[courseID] = Course(courseID, row[i], 3)

                    if batchID not in batches.keys():
                        batches[batchID] = Batch(batchID)
            break

    return teacherCourses


def applyHeuristics():
    global teachers
    print(teachers)
    # teachers = sorted(teachers)