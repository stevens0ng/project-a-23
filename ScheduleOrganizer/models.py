from django.db import models
from django.contrib.auth.models import User, AbstractUser
import requests, re


# Create your models here.
# class student(models.Model):
#     courses = models.ManyToManyField(course)

# https://www.dennisivy.com/post/django-class-based-views/

class assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank = True)
    title = models.CharField(max_length=30)
    due_date = models.CharField(max_length=30)
    description = models.TextField(null=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete', 'due_date']


class course(models.Model):
    users = models.ManyToManyField(User)
    id_num = models.CharField(max_length=100, default='null')
    name = models.CharField(max_length=100, default='null')
    letters = models.CharField(max_length=100, default='null')
    number = models.CharField(max_length=100, default='null')
    section = models.CharField(max_length=100, default='null')
    instructor = models.CharField(max_length=100, default='null')

    def __str__(self):
        return self.name

    # def __unicode__(self):

    #     return self.name

    # @classmethod
    # def create(cls, name):
    #     course = cls(name = name)
    #     return course


class courseAssignment(models.Model):
    course_class = models.ForeignKey(course, on_delete=models.CASCADE, null=True, blank = True)
    title = models.CharField(max_length=30)
    due_date = models.CharField(max_length=30)
    description = models.TextField(null=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete', 'due_date']


# creating instances of course object
def course_list_create():

    class_list = []
    url = 'https://api.devhub.virginia.edu/v1/courses'
    data = requests.get(url).json()

    for item in data["class_schedules"]["records"]:

        if item[0] == "CS" and item[12] == "2022 Spring" and item[1] < str(5000) and item[2] < str(100):
            class_items = [
                item[0] + " " + item[1] + ": " + item[4] + " - Section " + item[2],
                item[3],
                item[0],
                item[1],
                item[2],
                re.sub(r'(?<=[.,])(?=[^\s])', r' ', item[6]),
            ]

            class_list.append(class_items)

    names_lst = []
    for object in course.objects.all():
        names_lst.append(object.name)
    for course_item in class_list:

        # thing = course.create(course_item)
        if course_item[0] not in names_lst:
            course_itemx = course()
            setattr(course_itemx, 'name', course_item[0])
            setattr(course_itemx, 'id_num', course_item[1])
            setattr(course_itemx, 'letters', course_item[2])
            setattr(course_itemx, 'number', course_item[3])
            setattr(course_itemx, 'section', course_item[4])
            setattr(course_itemx, 'instructor', course_item[5])
            course_itemx.save()



class mycourse(models.Model):
    name = models.CharField(max_length=100, default='null')

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name):
        mycourse = cls(name = name)
        return mycourse


class schedule(models.Model):
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=100, default='null')
    instructor = models.CharField(max_length=100, default='null')
    days = models.CharField(max_length=15, default='null')
    time_start = models.CharField(max_length=15, default='null')
    time_end = models.CharField(max_length=15, default='null')
    def __str__(self):
        return self.name


def schedule_list_create():
    url = 'https://api.devhub.virginia.edu/v1/courses'
    data = requests.get(url).json()
    for item in data["class_schedules"]["records"]:
        if item[0] == "CS" and item[12] == "2022 Spring" and item[1] < str(5000) and item[2] < str(100):
            schedule_itemx = schedule()
            setattr(schedule_itemx, 'name', item[0] + " "+ item[1] + ": " + item[4] + " - Section " + item[2])
            setattr(schedule_itemx, 'instructor', item[6])
            if (item[8] == 'TR'):
                setattr(schedule_itemx, 'days', 'Thursday')
            elif (item[8] == 'W'):
                setattr(schedule_itemx, 'days', 'Wednesday')
            elif (item[8] == 'T'):
                setattr(schedule_itemx, 'days', 'Tuesday')
            elif (item[8] == 'M'):
                setattr(schedule_itemx, 'days', 'Monday')
            elif (item[8] == 'F'):
                setattr(schedule_itemx, 'days', 'Friday')
            else:
                setattr(schedule_itemx, 'days', item[8])
            setattr(schedule_itemx, 'time_start', item[9])
            setattr(schedule_itemx, 'time_end', item[10])
            schedule_itemx.save()


#course_list_create()
#schedule_list_create()



