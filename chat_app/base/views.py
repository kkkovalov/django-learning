from django.shortcuts import render

rooms = [
    {'id': 1, 'name': 'Lets learn Python'},
    {'id': 2, 'name': 'Lets teach Django'},
    {'id': 3, 'name': 'Front end questions'},
    {'id': 4, 'name': 'Why learn devOps'},
]

# Create your views here.
def home(request):
    context = {
        'rooms': rooms
    }
    return render(request, 'base/home.html', context=context)

def room(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    return render(request, 'base/room.html', context={'room': room})