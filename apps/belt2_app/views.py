from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
from datetime import date


def index(request):
    return render(request, 'belt2_app/dashboard.html')



def dashboard(request):
    print(request.session['user_id'])
    if 'user_id' not in request.session:
        return redirect('/')
    # if request.session['user_id'] != 0:
    #     return redirect('/')
    my_trips = Trip.objects.filter(traveler=request.session['user_id'])
    context = {
        'alltrips': Trip.objects.all(),
        'mytrips' : my_trips,
        'alltrips': Trip.objects.exclude(traveler=request.session['user_id']),
    }

    return render(request, 'belt2_app/dashboard.html', context)\



def addtrip(request):
    if request.method=='POST':
        
        created_by = User.objects.get(id=request.session['user_id'])

        errors = Trip.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/addtrip')

        created_by = User.objects.get(id=request.session['user_id'])
        trip = Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], start_date = request.POST['start_date'], end_date = request.POST['end_date'], created_by=created_by)
        trip.traveler.add(created_by)

        return redirect('/dashboard')

    elif request.method == 'GET':
        return render(request, 'belt2_app/addtrip.html')



def deletetrip(request, id):
    Trip.objects.get(id=id).delete()
    return redirect('/dashboard')



def join(request, id):
    if 'user_id' not in request.session:
        return redirect('/')

    this_traveler = User.objects.get(id=request.session['user_id'])
    this_trip = Trip.objects.get(id=id)
    this_traveler.trips.add(this_trip)

    return redirect('/dashboard')



def leave(request, id):
    if 'user_id' not in request.session:
        return redirect('/')

    this_traveler = User.objects.get(id=request.session['user_id'])
    this_trip = Trip.objects.get(id=id)
    this_traveler.trips.remove(this_trip)

    return redirect('/dashboard')



def viewtrip(request, id):
    trip = Trip.objects.get(id=id)

    context = {
        'id': id,
        'this_trip': trip,
        'destination': Trip.objects.get(id=id).destination,
        'description': Trip.objects.get(id=id).description,
        'start_date': Trip.objects.get(id=id).start_date,
        'end_date': Trip.objects.get(id=id).end_date,
        'created_at': Trip.objects.get(id=id).created_at,
        'updated_at': Trip.objects.get(id=id).updated_at
    }
    return render(request, 'belt2_app/trip.html', context)

