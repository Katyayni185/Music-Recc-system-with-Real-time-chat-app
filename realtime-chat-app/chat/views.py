from django.shortcuts import render, redirect
#to check whether room which is enterd by the user exist or not
from chat.models import Room, Message

from django.http import HttpResponse, JsonResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username') #name to of user
    #object.get will get the name of this particular room.
    room_details = Room.objects.get(name=room) 

    #passing all the deatils to our HTML
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username'] 
    #Check if name of the room already exists 
    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    #if the room does not exists then create new room
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    #We'll find room from where we have to get all the messages 
    room_details = Room.objects.get(name=room)

    #so now we have the room so we will be filtering all the messages with the room id.
    messages = Message.objects.filter(room=room_details.id)

    
    return JsonResponse({"messages":list(messages.values())})