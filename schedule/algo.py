# This method should return the final table
import datetime

# batchesList = {}
# batchesList = {}
# batchesList = {}

# Parent Function
def runAlgo(batchesList, coursesList, teachersList, SLOTS_PER_DAY, NUMBER_OF_CLASSES):
    # Initialize all necessary fields
    finalRoutine = []
    lockTeacher = [[], [], [], [], [], []]
    lockBatch = [[], [], [], [], [], []]        # For each slot of the day
    lockCourse = []

    currentNumberOfClasses = 0


    def pickTeacher(dayInd, slotInd, course, teacherInd):
        print('Teacher', teacherInd)

        if teacherInd == len(course.courseTeachers):
            return None

        # check if teacher can take class on this slotInd. True if yes, Flase if no
        teacher = course.courseTeachers[teacherInd]
        slot = SLOTS_PER_DAY[slotInd]
        courseFinish = slot + datetime.timedelta(hours=course.duration)

        if not teacher.available:
            print('T: Teacher Not Availble')
            if not course.isLabCourse:
                return pickTeacher(dayInd, slotInd, course, teacherInd+1)
            else:
                return None

        for teacherSlot in teacher.teacherSlots[dayInd]:
            if teacherSlot[0] <= slot and teacherSlot[1]>=courseFinish:
                return teacher
        
        print('T: Time didn\'t match', teacher.initial)
        if not course.isLabCourse:
            return pickTeacher(dayInd, slotInd, course, teacherInd+1)
        else:
            return None
        

    def pickCourse(dayInd, slotInd, courseInd):
        # print('len', len(batchesList.keys()), 'done, week', course.doneClass, course.weeklyClass)
        # print('Is Lab', course.isLabCourse)

        if courseInd == len(coursesList.keys()):
            return pickSlot(dayInd, slotInd+1)

        courseKeys = list(coursesList)
        course = coursesList[courseKeys[courseInd]]

        print('Course', course.id)

        def assignTeacher(teachersToBeAssigned):
            for t in teachersToBeAssigned:
                print('Assinging Teacher: ', t)
                if course.isLabCourse:
                    lockTeacher[slotInd+2].append(t)
                else:
                    lockTeacher[slotInd+1].append(t)
                t.available = False
                t.routine[dayInd][slotInd] = course

        def teacherFound(teachersToBeAssigned):
            print('Found Teacher')

            nonlocal currentNumberOfClasses

            # assignTeacher
            assignTeacher(teachersToBeAssigned)

            # Lock the batch
            batch = generateBatchCode(course.id)
            batchesList[batch].available = False

            # Lock the course
            course.doneClass = course.doneClass + 1
            course.available = False
            lockCourse.append(course)

            # Handle Lab Course
            if course.isLabCourse:
                lockBatch[slotInd+2].append(batch)
            else:
                lockBatch[slotInd+1].append(batch)

            # Increase counter of assigned classes
            currentNumberOfClasses = currentNumberOfClasses + 1

            if pickCourse(dayInd, slotInd, courseInd+1):
                return True
            else:
                batchesList[batch].available = True
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


        # If not possible, continue
        if course.doneClass == course.weeklyClass or \
            not batchesList[generateBatchCode(course.id)].available or \
                not course.available:
            return pickCourse(dayInd, slotInd, courseInd+1)

        # If lab course, assign multiple teachers together if needed

        teachersToBeAssignedTest = []

        if course.isLabCourse:
            possible = True
            
            for i in range(len(course.courseTeachers)):
                teacher = pickTeacher(dayInd, slotInd, course, i)
                if teacher != None:
                    teachersToBeAssignedTest.append(teacher)
                else:
                    possible = False
                    break
            
            if possible:
                teacherFound(teachersToBeAssignedTest)
            else:
                return pickCourse(dayInd, slotInd, courseInd+1)
        else:
            teacher =  pickTeacher(dayInd, slotInd, course, 0)
            if teacher == None:
                print('Cannot Pick Teacher')
                return pickCourse(dayInd, slotInd, courseInd+1)
            else:
                teachersToBeAssignedTest.append(teacher)
                teacherFound(teachersToBeAssignedTest)

                

    def pickSlot(dayInd, slotInd):
        print('Slot', slotInd)

        if currentNumberOfClasses == NUMBER_OF_CLASSES:
            # DEBUG
            print('Beacuse of this?')

            return True

        if slotInd == 5:
            return pickDay(dayInd+1)
        
        unlock(slotInd)
        
        if not pickCourse(dayInd, slotInd, 0):
            return pickSlot(dayInd, slotInd+1)
        
        else:
            return True

    def pickDay(dayInd):
        print('Day', dayInd, currentNumberOfClasses)
        unlockAll()

        if dayInd == 5:
            return False
        
        if not pickSlot(dayInd, 0):
            return pickDay(dayInd+1)
        else:
            return True

    def init(finalRoutine):
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
            batchesList[b].available = True
        lockBatch[slotInd].clear()
        for t in lockTeacher[slotInd]:
            t.available = True
        lockTeacher[slotInd].clear()

    def generateBatchCode(courseID):
        return int(courseID/1000) * 10

    # Function calls

    init(finalRoutine)
    if pickDay(0):
        print('It Worked!')
    else:
        print('Sorry no valid combination found!')

    return teachersList, coursesList