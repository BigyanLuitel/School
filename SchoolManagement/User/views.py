from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import User, Student, Teacher


def index(request):
    return render(request,'User/index.html')

def student_register(request):
    if request.method == "POST":
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        date_of_birth= request.POST.get('date_of_birth')
        username= request.POST.get('username')
        password= request.POST.get('password')
        email= request.POST.get('email')
        student_id= request.POST.get('student_id')
        grade= request.POST.get('grade')
        
        Student.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            date_of_birth=date_of_birth,
            password=password,
            email=email,
            student_id=student_id,
            grade=grade
        )
        students = Student.student.all()
        return redirect('/index/')
    context = {
        'students': Student.objects.all()
    }
                
    return render(request,'User/student_register.html',context)

def teacher_register(request):
    return render(request,'User/teacher_register.html')