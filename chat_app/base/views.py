from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, decorators, models, forms

from . import models, forms

# Create your views here.

def loginPage(request):
    
    page = "login"
    
    if request.user.is_authenticated:
        return redirect('home-page')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = models.User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home-page')
        else:
            messages.error(request, 'Username OR password does not exist')
    
    context = {
        'page': page,
        
    }
    return render(request, 'base/login_register.html', context=context)

def logoutUser(request):
    logout(request)
    return redirect('home-page')

def registerUser(request):
    form = forms.UserCreationForm()
    
    if request.method == "POST":
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home-page')
        else:
            messages.error(request, "An error occurred during registration")
            
    
    context = {
        'form': form
    }
    return render(request, 'base/login_register.html', context=context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    room_messages = models.Message.objects.all().filter(Q(room__topic__name__icontains=q))
    rooms = models.Room.objects.filter(
        Q(topic__name__contains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = models.Topic.objects.all()
    room_count = rooms.count()
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,
    }
    return render(request, 'base/home.html', context=context)

def room(request, pk):
    room = models.Room.objects.get(pk=pk)
    roomMessages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    
    if request.method == "POST":
        message = models.Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room-page', pk=room.id)
    
    context = {
        'room': room,
        'roomMessages': roomMessages,
        'participants': participants,
    }
    return render(request, 'base/room.html', context=context)

@decorators.login_required(login_url='/login')
def createRoom(request):
    form = forms.RoomForm()
    
    if request.method == 'POST':
        form = forms.RoomForm(request.POST)
        if form.is_valid():
            newRoom = form.save(commit=False)
            newRoom.host = request.user
            newRoom.save()
            return redirect('home-page')
        else:
            messages.error(request, "AN error has occurred, please try again!")
        
    
    context ={
        'form': form,
    }
    return render(request, 'base/room_form.html', context=context)

@decorators.login_required(login_url='/login')
def updateRoom(request, pk):
    room = models.Room.objects.get(pk=pk)
    form = forms.RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse("You are not allowed here!")
    
    if request.method == "POST":
        form = forms.RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home-page')
    
    context = {
        'form': form,
    }
    return render(request, 'base/room_form.html', context)

@decorators.login_required(login_url='/login')
def deleteRoom(request, pk):
    room = models.Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse("You are not allowed here!")
    
    if request.method == "POST":
        room.delete()
        return redirect('home-page')
    
    context = {
        "obj":   room
    }
    return render(request, 'base/delete.html', context=context)

@decorators.login_required(login_url='/login')
def deleteMessage(request, pk):
    message = models.Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse("You are not allowed here!")
    
    if request.method == "POST":
        message.delete()
        return redirect('home-page')
    
    context = {
        "obj":   message
    }
    return render(request, 'base/delete.html', context=context)


def userProfile(request, pk):
    user = models.User.objects.get(id=pk)
    rooms = user.room_set.all()
    roomMessages = user.message_set.all()
    topics = models.Topic.objects.all()
    context = {
    "user": user,
    "rooms": rooms,
    "roomMessages": roomMessages,
    "topics": topics
    }
    return render(request, 'base/profile.html', context=context)