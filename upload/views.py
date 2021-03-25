from django.shortcuts import render
from django.http import *
from .forms import *
from schedule.algo import schedule
import django_excel as excel

# Create your views here.

def upload_file(request):
    if(request.method == 'POST'):
        fileHandle = request.FILES['file']
        temp = fileHandle.get_book()

        sheet = fileHandle.get_book()[0]
        sheet = sheet.name_columns_by_row(1)

        schedule(fileHandle.get_book())
        return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})