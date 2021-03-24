from .models import *
from django import forms
from bootstrap_datepicker_plus import TimePickerInput, DatePickerInput

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = [
            'slots',
            'courses'
        ]

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ['slots']

class SlotForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = '__all__'
        widgets = {
            'startingTime': TimePickerInput(),
            'endingTime': TimePickerInput()
        }