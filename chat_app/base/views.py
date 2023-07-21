from django.shortcuts import render

from . import models

# rooms = [
#     {'id': 1, 'name': 'Lets learn Python'},
#     {'id': 2, 'name': 'Lets teach Django'},
#     {'id': 3, 'name': 'Front end questions'},
#     {'id': 4, 'name': 'Why learn devOps'},
# ]



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