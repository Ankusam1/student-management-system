from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from smsapp.models import Student
from django.http import HttpResponseForbidden


@login_required
def data(request):
    student_list = Student.objects.all().order_by('id')
    paginator = Paginator(student_list, 10)  # 10 students per page
    page_number = request.GET.get('page')
    students = paginator.get_page(page_number)

    total_students = Student.objects.count()

    total_bca = Student.objects.filter(course__iexact="BCA").count()
    total_mca = Student.objects.filter(course__iexact="MCA").count()

    context = {
        'students': students,
        'total_students': total_students,
        'total_bca': total_bca,
        'total_mca': total_mca
    }

    return render(request, 'index.html', context)


@login_required
def add_student(request):
    if request.method == "POST":
        roll = request.POST.get('roll_no')
        name = request.POST.get('name')
        email = request.POST.get('email')
        course = request.POST.get('course')
        phone = request.POST.get('phone_no')

        Student.objects.create(
            roll_no=roll,
            name=name,
            email=email,
            course=course,
            phone_no=phone
        )
        return redirect('home')

    return render(request, 'add_student.html')


@login_required
def edit_student(request, id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to edit.")

    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.roll_no = request.POST.get('roll_no')
        student.name = request.POST.get('name')
        student.email = request.POST.get('email')
        student.course = request.POST.get('course')
        student.phone_no = request.POST.get('phone_no')
        student.save()
        return redirect('home')

    return render(request, 'edit_student.html', {'student': student})


@login_required
def delete_student(request, id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to delete.")

    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('home')
