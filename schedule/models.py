from django.db import models

DAYS_OF_WEEK = (
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday'),
)

# Create your models here.

class Teacher(models.Model):
    initial = models.CharField(max_length=5, primary_key=True)
    full_name = models.CharField(max_length=50)
    designation = models.CharField(max_length=30)
    department = models.CharField(max_length=50)
    university = models.CharField(max_length=50)
    courses = models.ManyToManyField(Course)

class Student(models.Model):
    name = models.CharField(max_length=50)
    roll = models.PositiveIntegerField
    courses = models.ManyToManyField(Course)

class Course(models.Model):
    id = models.CharField('Course ID', max_length=30, primary_key=True)
    name = models.CharField(max_length=50)

class Slot(models.Model):
    day = models.CharField(max_length=1, choices=DAYS_OF_WEEK)
    startingTime = models.TimeField
    endingTime = models.TimeField