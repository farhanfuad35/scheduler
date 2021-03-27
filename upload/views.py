from django.shortcuts import render
from django.http import *
from .forms import *
from schedule.preprocess import schedule
import django_excel as excel

# Create your views here.

def upload_file(request):
    if(request.method == 'POST'):
        fileHandle = request.FILES['file']
        temp = fileHandle.get_book()

        sheet = fileHandle.get_book()[0]
        sheet = sheet.name_columns_by_row(1)
        
    # try:
        teachers, courses = schedule(fileHandle.get_book())
        
        teachersKeys = list(teachers.keys())
        print(teachers[teachersKeys[0]].routine[0])
    # except Exception:
        # return HttpResponse('<h1>Error occured, please check the input format!</h1>')
    # else:
        printRoutine(teachers)

        # No offence
        # processedTeachers = processTeacher(teachers, courses)
        context = {'teachers':teachers}
        return render(request, 'routine.html', status=200, context=context)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def processTeacher(teachers, courses):
    newTeachers = teachers
    newTeachersKeys = list(newTeachers)
    for key in newTeachersKeys:
        for course in newTeachers[key].courses:
            newTeachers[key]['Saturday'] = courses[course]
            newTeachers[key]['Monday'] = course[1]
            newTeachers[key]['Tuesday'] = course[2]
            newTeachers[key]['Wednesday'] = course[3]
            newTeachers[key]['Thursday'] = course[4]
    
    return newTeachers

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