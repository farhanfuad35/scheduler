def printRoutine(teachers):
    print(teachers)
    teacherKeys = list(teachers)
    for i in range(len(teacherKeys)):
        print('key: ' + teacherKeys[i])
        teacher = teachers[teacherKeys[i]]
        for i in range(5):
            for j in range(5):
                if teacher.routine[i][j] is None:
                    print('*', end=' | ')
                else:
                    section = ''
                    if teacher.routine[i][j].isLabCourse:
                        section = 'Section ' + str(int(teacher.routine[i][j].id%10))
                    print(int(teacher.routine[i][j].id/10), section, '(' + teacher.initial + ')', end=' | ')
                    # print(teacher.routine[i][j].name, end=' | ')
            print('\n--------------')