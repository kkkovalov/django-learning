from django.shortcuts import render, redirect

from . import models
from . import forms

# Create your views here.
def home(request):
    rooms = models.Room.objects.all()
    context = {
        'rooms': rooms
    }
    return render(request, 'base/home.html', context=context)

def room(request, pk):
    room = models.Room.objects.get(pk=pk)
    context = {
        'room': room,
    }
    return render(request, 'base/room.html', context=context)

def createRoom(request):
    form = forms.RoomForm()
    if request.method == 'POST':
        form = forms.RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home-page')
        
    
    context ={
        'form': form,
    }
    return render(request, 'base/room_form.html', context=context)


def updateRoom(request, pk):
    room = models.Room.objects.get(pk=pk)
    form = forms.RoomForm(instance=room)
    
    if request.method == "POST":
        form = forms.RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home-page')
    
    context = {
        'form': form,
    }
    return render(request, 'base/room_form.html', context)
    
def deleteRoom(request, pk):
    room = models.Room.objects.get(id=pk)
    
    if request.method == "POST":
        room.delete()
        return redirect('home-page')
    
    context = {
        "obj":   room
    }
    return render(request, 'base/delete.html', context=context)