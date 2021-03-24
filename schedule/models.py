from django.db import models

# Create your models here.

class Slot(models.Model):
    DAYS_OF_WEEK = (
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    )

    day = models.CharField(max_length=20, choices=DAYS_OF_WEEK)
    startingTime = models.TimeField('Starts')
    endingTime = models.TimeField('Ends')

class Course(models.Model):
    course_id = models.CharField('Course ID', max_length=30)
    name = models.CharField('Course Name', max_length=50)
    section = models.CharField('Section/Group', max_length=30, default='N/A', blank='True')
    class Meta:
        unique_together = ['id', 'section']

class Teacher(models.Model):
    initial = models.CharField(max_length=5, primary_key=True)
    full_name = models.CharField(max_length=50)
    designation = models.CharField(max_length=30)
    department = models.CharField(max_length=50)
    university = models.CharField(max_length=50)
    courses = models.ManyToManyField(Course)
    slots = models.ManyToManyField(Slot)

class Student(models.Model):
    name = models.CharField(max_length=50)
    roll = models.PositiveIntegerField
    courses = models.ManyToManyField(Course)