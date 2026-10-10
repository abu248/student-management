from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Student, Course
from .forms import StudentForm


@login_required
def dashboard(request):
    context = {
        'total_students': Student.objects.count(),
        'total_courses': Course.objects.count(),
        'recent_students': Student.objects.order_by('-admission_date', '-id')[:5],
    }
    return render(request, 'students/dashboard.html', context)


@login_required
def student_list(request):
    query = request.GET.get('q', '')
    students = Student.objects.select_related('course')
    if query:
        students = students.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(roll_number__icontains=query) |
            Q(email__icontains=query)
        )
    page_obj = Paginator(students, 10).get_page(request.GET.get('page'))
    return render(request, 'students/student_list.html',
                  {'page_obj': page_obj, 'query': query})


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})


@login_required
def student_create(request):
    form = StudentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Student added.')
        return redirect('student_list')
    return render(request, 'students/student_form.html',
                  {'form': form, 'title': 'Add Student'})


@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, request.FILES or None, instance=student)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Student updated.')
        return redirect('student_detail', pk=student.pk)
    return render(request, 'students/student_form.html',
                  {'form': form, 'title': 'Edit Student'})


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted.')
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})