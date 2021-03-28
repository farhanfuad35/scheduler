from django.shortcuts import render
from django.http import *
from .forms import *
from schedule.preprocess import schedule
from .utility import printRoutine
import django_excel as excel

# Create your views here.

def upload_file(request):
    if(request.method == 'POST'):
        fileHandle = request.FILES['file']
        temp = fileHandle.get_book()

        sheet = fileHandle.get_book()[0]
        sheet = sheet.name_columns_by_row(1)
        
        try:
            teachers, valid = schedule(fileHandle.get_book())
        except Exception:
            return HttpResponse('<h1>Error occured, please check the input format!</h1>')
        else:

            # No offence
            context = {'teachers':teachers, 'valid': valid}
            if valid:
                return render(request, 'routine.html', status=200, context=context)
            else:
                return render(request, 'routine.html', status=409, context=context)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})