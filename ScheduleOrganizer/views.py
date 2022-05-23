from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import assignment, course, mycourse, User, AbstractUser, schedule, courseAssignment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
#from django.shortcuts import render_to_response

import requests
import json

# minute 59 of https://www.youtube.com/watch?v=llbtoQTt4qw if we want to make login view better
# django import view LoginView has redirect_authenticated_user field
# there is also log out view if we want but we should be fine

course_url = ""
course_id = 1


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def logout_view(request):
    logout(request)
    return render(request, 'landingpage.html')


# https://www.dennisivy.com/post/django-class-based-views/

class AssignmentList(LoginRequiredMixin, ListView):
    model = assignment
    context_object_name = 'assignments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignments']=context['assignments'].filter(user=self.request.user)
        context['count']=context['assignments'].filter(complete=False)
        return context


class AssignmentDetail(LoginRequiredMixin, DetailView):
    model = assignment
    context_object_name = 'assignment'


class AssignmentCreate(LoginRequiredMixin, CreateView):
    model = assignment
    fields = ['title','description','complete', 'due_date']
    success_url = reverse_lazy('assignments')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AssignmentCreate, self).form_valid(form)


class AssignmentUpdate(LoginRequiredMixin, UpdateView):
    model = assignment
    fields = ['title','description','complete', 'due_date']
    success_url = reverse_lazy('assignments')


class AssignmentDelete(LoginRequiredMixin, DeleteView):
    model = assignment
    context_object_name = 'assignment'
    success_url = reverse_lazy('assignments')

# def course_list(request):
        
#         class_list = [""]
#         url = 'https://api.devhub.virginia.edu/v1/courses'
#         data = requests.get(url).json()

#         class_item = ""
#         for item in data["class_schedules"]["records"]:
#             if item[0] == "CS" and item[12] == "2022 Spring" and item[1] < str(5000) and item[2] < str(100):
#                 class_item = item[0] + " "+  item[1] + ": " + item[4] + " - Section " + item[2]
#                 class_list.append(class_item)
#             class_item = ""
#         return render(request, 'course_list.html', {"classes": class_list})


class CourseList(LoginRequiredMixin, ListView):
    model = course
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for course in context['courses']:
            if self.request.user in course.users.all() :
                context['courses']=context['courses'].exclude(name=course.name)
        return context


class MyCourseList(LoginRequiredMixin, ListView):
    model = course
    context_object_name = 'courses'
    template_name='ScheduleOrganizer/mycourse_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for course in context['courses']:
            if self.request.user not in course.users.all() :
                context['courses']=context['courses'].exclude(name=course.name)
        return context


# # #class and functions for adding course for a user
# class CourseDetailView(DetailView):
#     template_name = 'ScheduleOrganizer/course_list.html'

#     def get_object(self, *args, **kwargs):
#         slug = self.kwargs.get('slug')
#         print('hi')
#         return get_object_or_404(course, slug=slug)

#     def get(self, request, *args, **kwargs):
        
#         name = request.GET.get("pk")
#         course_item = course.objects.get(pk=pk)

#         if "add_class" in request.GET:
#             print("hi")

#         request.user.courses.add(course_item)

#         return redirect('courses')


def add_course(request):
    if request.method == "GET":
        
        #separating url parameters into course name and user id to be used as keys to access values of their respectice objects later
        parameters = request.GET['course'].split("?user=")
        course_name = parameters[0]
        user_name_id = parameters[1]

        #print(course.objects.filter(name=course_name).first())
        
        #getting specific instance of course object
        course_thing   = course.objects.filter(name=course_name).first()
        #showing contents of users field before

        #removing a user from users field and showing that no more users exist in field
        course_thing.users.remove(User.objects.get(id=user_name_id))

        #adding user again to show that user is able to be added to course
        course_thing.users.add(User.objects.get(id=user_name_id))
        
        ##getting specific instance of schedule
        schedule_thing = schedule.objects.filter(name=course_name).first()
        ##removing a user from users field and showing that no more users exist in field
        schedule_thing.users.remove(User.objects.get(id=user_name_id))
        ##adding user again to show that user is able to be added to course
        schedule_thing.users.add(User.objects.get(id=user_name_id))

        #return HttpResponseRedirect('/ScheduleOrganizer/course_list.html')
        return HttpResponseRedirect(reverse('courses'))


def remove_course(request):
    if request.method == "GET":
        # separating url parameters into course name and user id to be used as keys to access values of their respectice objects later
        parameters = request.GET['course'].split("?user=")
        course_name = parameters[0]
        user_name_id = parameters[1]

        # print(course.objects.filter(name=course_name).first())

        # getting specific instance of course object
        course_thing = course.objects.filter(name=course_name).first()
        # showing contents of users field before

        # removing user again to show that user is able to be added to course
        course_thing.users.remove(User.objects.get(id=user_name_id))

        ## getting specific instance of schedule object
        schedule_thing = schedule.objects.filter(name=course_name).first()
        ## removing user again to show that user is able to be added to schedule
        schedule_thing.users.remove(User.objects.get(id=user_name_id))

        # return HttpResponseRedirect('/ScheduleOrganizer/course_list.html')
        return HttpResponseRedirect(reverse('mycourses'))


#create assignments for each individual courses
class CourseAssignmentList(LoginRequiredMixin, ListView):
    model = courseAssignment
    context_object_name = 'courseAssignments'
    template_name = 'ScheduleOrganizer/courseAssignment_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #filter by course
        #course_url = self.request.META.get('HTTP_REFERER')
        global course_url
        course_url = self.request.get_full_path()
        
        context['courseAssignments']=context['courseAssignments'].filter(course_class=course.objects.filter(id=self.kwargs['pk']).first())
        context['count']=context['courseAssignments'].filter(complete=False)
        return context


class CourseAssignmentDetail(LoginRequiredMixin, DetailView):
    model = courseAssignment
    context_object_name = 'courseAssignment'
    template_name = 'ScheduleOrganizer/courseAssignment_detail.html'


class CourseAssignmentCreate(LoginRequiredMixin, CreateView):
    model = courseAssignment
    fields = ['title','description','complete', 'due_date']

    #global course_id
    #success_url = reverse_lazy('courseAssignment-list', kwargs={'pk':course_url[9:len(course_url)-1]})
    template_name = 'ScheduleOrganizer/courseAssignment_form.html'
    def get_success_url(self):
        print("PRINTPDDF", self.request.path)
        return reverse_lazy('courseAssignment-list', kwargs={'pk':course_id})

    def form_valid(self, form):
        global course_url
        global course_id
        #add for a course
        #global course_id
        course_id = course_url[9:len(course_url)-1]
        
        print("printing", course_id)

        courseAssignmentInstance = form.save(commit=False)
        print("heloooo", course.objects.filter(id=course_id))
        
        courseAssignmentInstance.course_class = course.objects.filter(id=course_id).first()
        #courseAssignmentInstance.save()
        return super(CourseAssignmentCreate, self).form_valid(form)


class CourseAssignmentUpdate(LoginRequiredMixin, UpdateView):
    model = courseAssignment
    fields = ['title','description','complete', 'due_date']
    #success_url = reverse_lazy('courseAssignment-list')
    #success_url = reverse_lazy('courses')
    template_name = 'ScheduleOrganizer/courseAssignment_form.html'

    def get_success_url(self):
        global course_url
        # global course_id
        # add for a course
        global course_id
        course_id = course_url[9:len(course_url) - 1]

        return reverse_lazy('courseAssignment-list', kwargs={'pk': course_id})



class CourseAssignmentDelete(LoginRequiredMixin, DeleteView):
    model = courseAssignment
    context_object_name = 'courseAssignment'
    #success_url = reverse_lazy('courseAssignment-list')
    #success_url = reverse_lazy('courseAssignment-list', kwargs={'pk':course_id})
    #success_url = reverse_lazy('courseAssignment-list')
    template_name = 'ScheduleOrganizer/courseAssignment_confirm_delete.html'
    def get_success_url(self):
        
        global course_url
        #global course_id
        #add for a course
        global course_id
        course_id = course_url[9:len(course_url)-1]
        
        return reverse_lazy('courseAssignment-list', kwargs={'pk':course_id})
        

def myschedule(request):
    schedules = schedule.objects.all()
    monS = list()
    tueS = list()
    wedS = list()
    thuS = list()
    friS = list()
    mymonS = list()
    mytueS = list()
    mywedS = list()
    mythuS = list()
    myfriS = list()

    for item in schedules:
        if ('Thursday' in item.days or 'TR' in item.days):
            thuS.append(item)
            if request.user in item.users.all() :
                mythuS.append(item)
        elif ('T' in item.days):
            tueS.append(item)
            if request.user in item.users.all() :
                mytueS.append(item)
        else:
            if ('M' in item.days):
                monS.append(item)
                if request.user in item.users.all() :
                    mymonS.append(item)
            if ('W' in item.days):
                wedS.append(item)
                if request.user in item.users.all() :
                    mywedS.append(item)
            if ('F' in item.days):
                friS.append(item)
                if request.user in item.users.all() :
                    myfriS.append(item)

    context = {'monS': monS, 'tueS': tueS, 'wedS': wedS, 'thuS': thuS, 'friS': friS, 'mymonS': mymonS, 'mytueS': mytueS, 'mywedS': mywedS, 'mythuS': mythuS, 'myfriS': myfriS}
    return render(request, 'ScheduleOrganizer/myschedule.html', context)