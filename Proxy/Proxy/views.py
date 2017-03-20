from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render

def prof_home(request):
    # add context as third arg to render
    return render(request, 'prof_home.html')

def prof_course(request):
    # add context as third arg to render
    return render(request, 'prof_course.html')

def add_stud(request):
    # add context as third arg to render
    return render(request, 'add_stud.html')

def daily_report(request):
    # add context as third arg to render
    return render(request, 'daily_report.html')

def prof_history(request):
    # add context as third arg to render
    return render(request, 'prof_history.html')

def take_attendance(request):
    # add context as third arg to render
    return render(request, 'take_attendance.html')

def prof_queries(request):
    # add context as third arg to render
    return render(request, 'prof_queries.html')      
