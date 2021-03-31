# This method returns the final teachers Set which contains routines for each teacher
import datetime

# Parent Function
def runAlgo(batchesList, coursesList, teachersList, SLOTS_PER_DAY, NUMBER_OF_CLASSES):
    # Initialize all necessary fields

    # CONSTANTS
    MEMO = set()
    CLASS_START = datetime.datetime.strptime('08:30 AM', '%I:%M %p')
    CLASS_END = datetime.datetime.strptime('05:00 PM', '%I:%M %p')

    # Keeps track of current routine state to avoid unnecessary duplicate recursion (Memoization)
    currentRoutineState = ''

    finalRoutine = []
    lockTeacher = [[], [], [], [], [], []]
    lockBatch = [[], [], [], [], [], []]        # For each slot of the day. Contains Batch ID, not Batch
    lockCourse = []

    currentNumberOfClasses = 0


    def pickTeacher(dayInd, slotInd, course, teacherInd):
        # print('Teacher', teacherInd)
        nonlocal CLASS_END

        if teacherInd == len(course.courseTeachers):
            return None

        # check if teacher can take class on this slotInd. True if yes, Flase if no
        teacher = course.courseTeachers[teacherInd]
        slot = SLOTS_PER_DAY[slotInd]
        courseFinish = slot + course.duration

        def proceed():
            if not course.isLabCourse:
                return pickTeacher(dayInd, slotInd, course, teacherInd+1)
            else:
                return None

        if not teacher.available or courseFinish > CLASS_END:
            return proceed()

        for teacherSlot in teacher.teacherSlots[dayInd]:
            if teacherSlot[0] <= slot and teacherSlot[1]>=courseFinish:
                return teacher

        return proceed()
        

    def pickCourse(dayInd, slotInd, courseInd):
        if courseInd == len(coursesList.keys()):
            return pickSlot(dayInd, slotInd+1)

        courseKeys = list(coursesList)
        course = coursesList[courseKeys[courseInd]]

        # print('Course', course.id)

        def assignTeacher(teachersToBeAssigned):
            # Update the routine

            for t in teachersToBeAssigned:
                # print('Found Teacher:', t.initial)
                if course.isLabCourse:
                    lockTeacher[slotInd+2].append(t)
                else:
                    lockTeacher[slotInd+1].append(t)
                t.available = False
                t.routine[dayInd][slotInd] = course

        def unAssignTeacher(teachersToBeUnassigned):
            for t in teachersToBeUnassigned:
                try:
                    if course.isLabCourse:
                        lockTeacher[slotInd+2].remove(t)
                    else:
                        lockTeacher[slotInd+1].remove(t)
                except:
                    pass
                t.available = True
                t.routine[dayInd][slotInd] = None



        def teacherFound(teachersToBeAssigned):
            nonlocal currentNumberOfClasses
            nonlocal currentRoutineState

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
                batchesList[batch].inLabClass = True
            else:
                lockBatch[slotInd+1].append(batch)

            # Increase counter of assigned classes
            currentNumberOfClasses = currentNumberOfClasses + 1

            # Update Current Routine State
            adderString = 'D' + str(dayInd) + 'S' + str(slotInd) + 'C' + str(courseInd)
            currentRoutineState = currentRoutineState + adderString

            # Return True if it works
            if pickCourse(dayInd, slotInd, courseInd+1):
                return True

            # Undo everything here if this assignment doesn't workout            
            else:
                batchesList[batch].available = True
                course.available = True
                unAssignTeacher(teachersToBeAssigned)
                try:
                    lockCourse.remove(course)
                except:
                    pass
                course.doneClass = course.doneClass - 1
                currentNumberOfClasses = currentNumberOfClasses - 1

                # Undo currentRoutineState String
                currentRoutineState = currentRoutineState[:-len(adderString)]

                if course.isLabCourse:
                    try:
                        lockBatch[slotInd+2].remove(batch)
                        batchesList[batch].inLabClass = False
                    except:
                        pass
                else:
                    try:
                        lockBatch[slotInd+1].remove(batch)
                    except:
                        pass
                    
                
                return False


        # Parent Function Starts Here
        key = currentRoutineState + 'D' + str(dayInd) + 'S' + str(slotInd) + 'C' + str(courseInd)
        
        if key in MEMO:
            return False
        
        else:
            # If not possible, continue
            batch = batchesList[generateBatchCode(course.id)]

            # If the batch is currently unavailable but it's a lab course, then it may still be scheduled
            # if the batch is actually busy in a lab class. Meaning current lab course is for
            # a different section. What happens if it's not a different section? Then course.available becomes True
            # and this batch is skipped anyway
            if course.doneClass == course.weeklyClass or \
                (not batch.available and not course.isLabCourse) or \
                    (course.isLabCourse and not batch.available and not batch.inLabClass) or \
                    not course.available:
                result = pickCourse(dayInd, slotInd, courseInd+1)

            # If lab course, assign multiple teachers together if needed

            elif course.isLabCourse:
                teachersToBeAssignedTest = []
                possible = True
                
                for i in range(len(course.courseTeachers)):
                    teacher = pickTeacher(dayInd, slotInd, course, i)
                    if teacher != None:
                        teachersToBeAssignedTest.append(teacher)
                    else:
                        possible = False
                        break
                
                if possible:
                    result = teacherFound(teachersToBeAssignedTest)
                else:
                    result = pickCourse(dayInd, slotInd, courseInd+1)
            else:
                teachersToBeAssignedTest = []
                teacher =  pickTeacher(dayInd, slotInd, course, 0)
                if teacher == None:
                    result = pickCourse(dayInd, slotInd, courseInd+1)
                else:
                    teachersToBeAssignedTest.append(teacher)
                    result = teacherFound(teachersToBeAssignedTest)
            
            MEMO.add(key)

            return result

                

    def pickSlot(dayInd, slotInd):
        # print('DayInd = {}, Slot = {}'.format(dayInd, slotInd))

        key = currentRoutineState + 'D' + str(dayInd) + 'S' + str(slotInd)

        if currentNumberOfClasses == NUMBER_OF_CLASSES:
            return True

        if slotInd == 5:
            return pickDay(dayInd+1)
        
        unlock(slotInd)
        
        if key in MEMO:
            return False
        else:
            result = pickCourse(dayInd, slotInd, 0)
            MEMO.add(key)
            if result is False:
                return pickSlot(dayInd, slotInd+1)
            
            else:
                return True

    def pickDay(dayInd):
        key = currentRoutineState + 'D' + str(dayInd)
        # print('Day', dayInd, 'Routine State: ', currentRoutineState)
        unlockAll()

        if dayInd == 5:
            return False
        
        if key not in MEMO:
            result = pickSlot(dayInd, 0)
            MEMO.add(key)
            if result is False:
                return pickDay(dayInd+1)
            else:
                return True

        # It is assumed that the ouput is just a single valid routine.
        # Thus, just the info if this combination has already been checked
        # before is saved. If the unique string is found in the MEMO list,
        # it means, this combination has been checked before and implies
        # a valid routine was not found. But if all possible valid routines
        # are expected, then the unique string should be saved along with it's
        # result (True/False) in a MEMO dictionary. Change this line in all
        # pick methods

        else:
            return False

    # ----------------
    # HELPER FUNCTIONS
    # ----------------       

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
            batchesList[b].inLabClass = False
        lockBatch[slotInd].clear()
        for t in lockTeacher[slotInd]:
            t.available = True
        lockTeacher[slotInd].clear()

    def generateBatchCode(courseID):
        return int(courseID/1000) * 10

    # -------------
    # OPTIMIZATIONS
    # -------------

    def teacherFreeHoursMoreThanCourseHours():
        teacherKeys = list(teachersList)
        for key in teacherKeys:
            if teachersList[key].totalSlotHours < teachersList[key].totalCourseHours:
                return False
        return True

    def preliminaryTest():
        return teacherFreeHoursMoreThanCourseHours()

    # Function calls

    init(finalRoutine)
    if preliminaryTest():
        valid = pickDay(0)
    else:
        valid = False

    return teachersList, valid