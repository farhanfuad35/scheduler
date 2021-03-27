# This method should return the final table
import datetime

batches = {}
courses = {}
teachers = {}

SLOTS_PER_DAY = ()
NUMBER_OF_CLASSES = 0
currentNumberOfClasses = 0

finalRoutine = []
lockTeacher = [[], [], [], [], [], []]
lockBatch = [[], [], [], [], [], []]        # For each slot of the day
lockCourse = []

def pickTeacher(dayInd, slotInd, course, teacherInd):
    print('Teacher', teacherInd)

    if teacherInd == len(teachers):
        return False

    # check if teacher can take class on this slotInd. True if yes, Flase if no
    teacherKeys = list(teachers)
    teacher = teachers[teacherKeys[teacherInd]]
    slot = SLOTS_PER_DAY[slotInd]
    courseFinish = slot + datetime.timedelta(hours=course.duration)

    if not teacher.available:
        print('T: Teacher Not Availble')
        return pickTeacher(dayInd, slotInd, course, teacherInd+1)

    for teacherSlot in teacher.teacherSlots[dayInd]:
        print('T: ', teacherSlot[0], teacherSlot[1], slot, courseFinish)
        if teacherSlot[0] <= slot and teacherSlot[1]>=courseFinish:
            lockTeacher[slotInd+1].append(teacher)
            teacher.available = False
            teacher.routine[dayInd][slotInd] = course
            return True
    
    print('T: Time didn\'t match', teacher.initial)
    return pickTeacher(dayInd, slotInd, course, teacherInd+1)
    

def pickCourse(dayInd, slotInd, courseInd):
    global currentNumberOfClasses

    # print('len', len(courses.keys()), 'done, week', course.doneClass, course.weeklyClass)
    # print('Is Lab', course.isLabCourse)

    if courseInd == len(courses.keys()):
        return pickSlot(dayInd, slotInd+1)

    courseKeys = list(courses)
    course = courses[courseKeys[courseInd]]

    print('Course', course.id)

    if course.doneClass == course.weeklyClass:
        print('Weekly class done')
        return pickCourse(dayInd, slotInd, courseInd+1)
    # print('Course Availability', course.available)
    if not batches[generateBatchCode(course.id)].available or not course.available:
        print('Not Available', batches[generateBatchCode(course.id)].available, course.available)
        return pickCourse(dayInd, slotInd, courseInd+1)
    if not pickTeacher(dayInd, slotInd, course, 0):
        print('Cannot Pick Teacher')
        return pickCourse(dayInd, slotInd, courseInd+1)
    else:
        print('Found Teacher')
        batch = generateBatchCode(course.id)
        batches[batch].available = False
        course.doneClass = course.doneClass + 1
        course.available = False
        lockCourse.append(course)
        if course.isLabCourse:
            lockBatch[slotInd+2].append(batch)
        else:
            lockBatch[slotInd+1].append(batch)
        currentNumberOfClasses = currentNumberOfClasses + 1

        if pickSlot(dayInd, slotInd+1):
            return True
        else:
            batches[batch].available = True
            course.available = True
            try:
                lockCourse.remove(course)
            except:
                pass
            course.doneClass = course.doneClass - 1
            currentNumberOfClasses = currentNumberOfClasses - 1
            if course.isLabCourse:
                try:
                    lockBatch[slotInd+2].remove(batch)
                except:
                    pass
            else:
                try:
                    lockBatch[slotInd+1].remove(batch)
                except:
                    pass
                
            
            return False
            

def pickSlot(dayInd, slotInd):
    print('Slot', slotInd)


    if currentNumberOfClasses == NUMBER_OF_CLASSES:
        return True

    if slotInd == 5:
        return pickDay(dayInd+1)
    
    unlock(slotInd)
    
    if not pickCourse(dayInd, slotInd, 0):
        return pickSlot(dayInd, slotInd+1)
    
    else:
        return True

def pickDay(dayInd):
    print('Day', dayInd)
    # print('-----------')
    # for i in range(dayInd):
    #     for j in range(5):
    #         print(finalRoutine[i][j])


    unlockAll()

    if dayInd == 5:
        return False
    
    if not pickSlot(dayInd, 0):
        return pickDay(dayInd+1)
    else:
        return True

def runAlgo(b, c, t, spd, noc):
    global batches
    global courses
    global teachers
    global SLOTS_PER_DAY
    global NUMBER_OF_CLASSES

    init()

    batches = b
    courses = c
    teachers = t
    SLOTS_PER_DAY = spd
    NUMBER_OF_CLASSES = noc

    if pickDay(0):
        print('It Worked!')
    else:
        print('Sorry no valid combination found!')

    return teachers

def init():
    for i in range(5):
        arr = [None, None, None, None, None]
        finalRoutine.append(arr)

def unlockAll():
    for i in range(6):
        unlock(i)
    
    for c in lockCourse:
        c.available = True
    lockCourse.clear()

def unlock(slotInd):
    for b in lockBatch[slotInd]:
        batches[b].available = True
    lockBatch[slotInd].clear()
    for t in lockTeacher[slotInd]:
        t.available = True
    lockTeacher[slotInd].clear()

def generateBatchCode(courseID):
    return int(courseID/1000) * 10