"""a23website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from . import views
from .views import AssignmentList, CourseList, add_course
import re 

urlpatterns = [
    path('', views.index, name="index"),
    path('assignments',views.AssignmentList.as_view(), name="assignments"),
    path('assignments/<int:pk>/', views.AssignmentDetail.as_view(), name = 'assignemnt'),
    path('assignments/assignment-create', views.AssignmentCreate.as_view(), name = 'assignment-create'),
    path('assignments/assignment-update/<int:pk>', views.AssignmentUpdate.as_view(), name = 'assignment-update'),
    path('assignments/assignment-delete/<int:pk>', views.AssignmentDelete.as_view(), name = 'assignment-delete'),
    path('courses',views.CourseList.as_view(), name="courses"),
    path('mycourses', views.MyCourseList.as_view(), name='mycourses'),
    path('add_course', views.add_course, name='add_course'),
    path('remove_course', views.remove_course, name='remove_course'),
    #path('course/courseAssignments/<int:pk>/', views.CourseAssignmentList.as_view(),name = 'courseAssignment'),
    path('courses/<int:pk>/', views.CourseAssignmentList.as_view(),name = 'courseAssignment-list'),
    path('courses/<int:pk>/<int:assignmentId>/', views.CourseAssignmentDetail.as_view(), name = 'courseAssignemnt'),
    #path('courses/<int:assignmentId>/', views.CourseAssignmentDetail.as_view(), name = 'courseAssignemnt'),
    path('courseAssignment-create', views.CourseAssignmentCreate.as_view(), name = 'courseAssignment-create'),
    path('courses/<int:courseID>/courseAssignment-update/<int:pk>', views.CourseAssignmentUpdate.as_view(), name = 'courseAssignment-update'),
    #path('courses/<int:courseID>/courseAssignment-delete/<int:pk>', views.CourseAssignmentDelete.as_view(), name = 'courseAssignment-delete'),
    path('courses/courseAssignment-delete/<int:pk>', views.CourseAssignmentDelete.as_view(), name = 'courseAssignment-delete'),
    # path('courses/<int:courseID>/courseAssignment-create', views.CourseAssignmentCreate.as_view(), name = 'courseAssignment-create'),
    # path('courses/<int:courseID>/courseAssignment-update/<int:pk>', views.CourseAssignmentUpdate.as_view(), name = 'courseAssignment-update'),
    # path('courses/<int:courseID>/courseAssignment-delete/<int:pk>', views.CourseAssignmentDelete.as_view(), name = 'courseAssignment-delete'),
    #re_path(r'add_course(/(?P<course>\w+)/(?P<user>\w+)/$)', views.add_course, name='add_course')
    path('myschedule', views.myschedule, name='myschedule'),
    path('custom_logout', views.logout_view),
]