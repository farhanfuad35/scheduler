from django.urls import path
from .views import *
from .forms import *

app_name = 'schedule'
urlpatterns = [
    path('', ScheduleWizard.as_view([SlotForm, CourseForm, TeacherForm])),
]