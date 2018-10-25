from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
from datetime import date


def index(request):
    if not "user_id" in request.session:
        request.session['user_id'] = 0
    if request.session['user_id'] != 0:
        return redirect('/')

    return render(request,'belt_app/index.html')



def register(request):
    if not "user_id" in request.session:
        request.session['user_id'] = 0
    if request.session['user_id'] != 0:
        return redirect('/')

    if request.method=='POST':
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')

        else:

            hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            just_registered = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashedpw.decode())
            request.session['user'] = just_registered.first_name
            request.session['user_id'] = just_registered.id
    return redirect('/')



def login(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.session['user_id'] != 0:
        return redirect('/')

    if request.method =='POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

    if request.method =='POST':
        user_logging_in = User.objects.filter(email=request.POST['lemail'])
        if len(user_logging_in) == 0:
            messages.error(request,'No matching user.')
            return redirect('/')
        elif not bcrypt.checkpw(request.POST['lpassword'].encode(), user_logging_in[0].password.encode()):
            messages.error(request,'Password is incorrect.')
            return redirect('/')
        else:
            request.session['user']= user_logging_in[0].first_name
            request.session['user_id']= user_logging_in[0].id
            return redirect('/dashboard')


def logout(request):
    request.session.clear()
    messages.add_message(request, messages.INFO, 'You have successfully been logged out.')
    return redirect('/')

