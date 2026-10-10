from django.contrib import admin
from .models import Course, Student


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'duration_months')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'full_name', 'email', 'course')
    list_filter = ('course', 'gender')
    search_fields = ('roll_number', 'first_name', 'last_name', 'email')