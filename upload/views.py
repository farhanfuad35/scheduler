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

        teachers = schedule(fileHandle.get_book())

        printRoutine(teachers)

        return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


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
            print('\n--------------')