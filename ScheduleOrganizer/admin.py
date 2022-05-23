from django.contrib import admin

# Register your models here.
from.models import assignment
from.models import course
from.models import courseAssignment

admin.site.register(assignment)
admin.site.register(course)
admin.site.register(courseAssignment)

