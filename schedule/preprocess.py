# We need to know if teacher i is available on day d at slot s. bool teachers[i].days[d][s]
# groupFree[302][1] = True : group 302 (Year 3, Semester 0, Section 2) is free (True) on Monday (1)

# In Teacher, courses[302] = 4 : courses 

import datetime
import django_excel as excel
from .algo import runAlgo

NUMBER_OF_SLOTS = 5
SLOTS_PER_DAY = (
        datetime.datetime.strptime('08:30 AM', '%I:%M %p'),
        datetime.datetime.strptime('10:00 AM', '%I:%M %p'),
        datetime.datetime.strptime('11:30 AM', '%I:%M %p'),
        datetime.datetime.strptime('02:00 PM', '%I:%M %p'),
        datetime.datetime.strptime('03:30 PM', '%I:%M %p')
    )

class Teacher:
    def __init__(self, initial, teacherSlots, courses, freeSlotHours, courseHours):
        self.initial = initial
        self.totalSlotHours = freeSlotHours
        self.totalCourseHours = courseHours
        self.name = None
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
        self.inLabClass = False
        
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
        self.duration = datetime.timedelta(hours=1.5)
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
            self.duration = datetime.timedelta(hours=3)


    def __str__(self):
        if self.isLabCourse:
            lab = 'Lab Course'
        else:
            lab = 'Not a lab course'
        return 'Course id: ' + str(self.id) + '\nCredit: ' + str(self.credit) + '\n' + lab + '\nWeekly Class: ' + str(self.weeklyClass)
        

def schedule(book):
    teachersList = {}
    coursesList = {}
    batchesList = {}

# Convert excel to python objects

    def preProcess(book):
        timetable = book[2].get_array()
        timetable.pop(0)
        for rec in timetable:
            initial = rec[0]
            teacherSlots = []
            freeSlotHour = datetime.timedelta(0)
            for day in range(2, 7):
                [slot, freeSlotHourPerDay] = convertToTime(rec[day])
                freeSlotHour = freeSlotHour + freeSlotHourPerDay
                teacherSlots.append(slot)

            courses, courseHours = getTeacherCourses(book, initial)
            teacher = Teacher(initial, teacherSlots, courses, freeSlotHour, courseHours)

            setCourseTeacher(teacher)
            teachersList[initial] = teacher

    def setCourseTeacher(teacher):
        for course in teacher.courses:
            coursesList[course].courseTeachers.append(teacher)

    def numberOfClasses():
        n=0
        for key in coursesList.keys():
            n = n + coursesList[key].weeklyClass
        return n

    def convertToTime(str):
        timeStrArr = str.split(';')
        ret = []
        freeSlotHour = datetime.timedelta(hours=0)
        for t in timeStrArr:
            try:
                startTime = t.split('-')[0]
                startTime = datetime.datetime.strptime(startTime, '%I:%M%p')
                endTime = t.split('-')[1]
                endTime = datetime.datetime.strptime(endTime, '%I:%M%p')
                ret.append([startTime, endTime])
                freeSlotHour = freeSlotHour + (endTime - startTime)
            except ValueError:
                pass
        
        return ret, freeSlotHour

    # Convert courses to id. CSE 3201 would be converted into 320 (3: Year, 2: Semester, 0: No Section)
    # CSE 3102 Section 2 would be converted into 312 (3: Year, 1: Semester, 2: Section)

    # This method also generates batch array and courses array while reading courses from the excel

    def getTeacherCourses(book, initial):

        sheet = book[1].get_array()
        teacherCourses = []

        # counts how many hours it's going to take to take all the courses a particular teacher is assigned to take
        courseHours = datetime.timedelta(0)
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
                        if courseID not in coursesList.keys():
                            coursesList[courseID] = Course(courseID, row[i], 3)

                        if batchID not in batchesList.keys():
                            batchesList[batchID] = Batch(batchID)

                        courseHours = courseHours + coursesList[courseID].duration * coursesList[courseID].weeklyClass
                break

        return teacherCourses, courseHours


    # def applyHeuristics():
    #     global teachers
    #     print(teachers)
        # teachers = sorted(teachers)

    def setTeacherNames(book):
        sheet = book[0].get_array()
        for row in sheet:
            if row[0] in teachersList.keys():
                teachersList[row[0]].name = row[1]


    preProcess(book)
    setTeacherNames(book)
    # applyHeuristics()

    return runAlgo(batchesList, coursesList, teachersList, SLOTS_PER_DAY, numberOfClasses())