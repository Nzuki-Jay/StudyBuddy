import json
from django.shortcuts import render, redirect
from .models import Room, Topic, Message, UserProfile, Reply
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.


def login_user(request):
    page = 'login'
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            message = 'Invalid Username/Password'

    context = {
        'page': page,
        'form': form,
        'message': message,
    }

    return render(request, 'core/login-register.html', context)


def register_user(request):
    page = 'register'
    message = ''
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(username, email, password)
            user_profile = UserProfile.objects.create(user=user)
            return redirect('login')
        else:
            message = 'Invalid Details'

    context = {
        'form': form,
        'page': page,
        'message': message,

    }
    return render(request, 'core/login-register.html', context)


def logout_user(request):
    logout(request)
    return redirect('index')


def index(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    rooms_count = rooms.count()
    topics_count = topics.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    user_profile = None
    if request.user.is_authenticated:
        if request.user.userprofile:
            user_profile = UserProfile.objects.get(user=request.user)
        else:
            user_profile = None

    form = ProfileForm(request.POST, request.FILES, instance=user_profile)
    context = {
        "rooms": rooms,
        "topics": topics,
        "rooms_count": rooms_count,
        "topics_count": topics_count,
        "room_messages": room_messages,
        "form": form,
    }
    return render(request, 'core/index.html', context)


@login_required(login_url='login')
def room(request, pk):
    user_profile = UserProfile.objects.get(user=request.user)
    form = ProfileForm(request.POST, request.FILES, instance=user_profile)
    topics = Topic.objects.all()
    topics_count = topics.count()
    the_room = Room.objects.get(pk=pk)
    room_messages = Message.objects.filter(room=the_room)
    participants = the_room.participants.all()
    if request.method == "POST":
        body = request.POST.get('message')
        message = Message.objects.create(user=request.user,
                                         room=the_room,
                                         body=body)
        the_room.participants.add(request.user)
        return redirect('room', pk=the_room.id)

    context = {
        "the_room": the_room,
        "room_messages": room_messages,
        "participants": participants,
        "topics_count": topics_count,
        "topics": topics,
        "form": form,

    }
    return render(request, 'core/the room.html', context)


def delete_message(request):
    if request.method == 'POST':
        message_id = request.POST.get('delete-message')
        message = Message.objects.get(id=message_id)
        message.delete()

    return redirect('room', pk=message.room.id)


@login_required(login_url='login')
def create_room(request):
    if request.method == "POST":
        name = request.POST.get('name')
        topic = request.POST.get('topic')
        description = request.POST.get('description')
        existing_topic = Topic.objects.filter(name=topic).first()

        if existing_topic:
            topic = existing_topic
        else:
            topic = Topic.objects.create(name=topic)
        new_room = Room.objects.create(
            host=request.user,
            topic=topic,
            name=name,
            description=description
        )
        return JsonResponse({'success': True,
                             'message': 'Room created successfully'})

    return redirect('index')


@login_required(login_url='login')
def profile(request, pk):
    user_profile = UserProfile.objects.get(user=request.user)
    form = ProfileForm(request.POST, request.FILES, instance=user_profile)
    user = User.objects.get(pk=pk)
    user_profile = UserProfile.objects.get(user=user)
    rooms = Room.objects.filter(host=user)
    messages = Message.objects.filter(user=user)
    topics = Topic.objects.all()
    topics_count = topics.count()

    context = {
        "user_profile": user_profile,
        "user": user,
        "rooms": rooms,
        "messages": messages,
        "topics_count": topics_count,
        "topics": topics,
        "form": form,
    }

    return render(request, 'core/profile.html', context)


def update_room(request, pk):
    room = Room.objects.get(pk=pk)

    if request.method == "POST":
        try:
            room.name = request.POST.get('name')
            room.description = request.POST.get('description')

            # Get the topic data by name, assuming you're sending the topic name in the form
            topic_name = request.POST.get('topic')
            existing_topic = Topic.objects.filter(name=topic_name).first()
            if existing_topic:
                room.topic = existing_topic
            else:
                new_topic = Topic.objects.create(name=topic_name)
                room.topic = new_topic

            room.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    topic_data = {
        'id': room.topic.id,
        'name': room.topic.name,

    }
    room_data = {
        'name': room.name,
        'topic': topic_data,  # Include the topic data
        'description': room.description,
    }
    return JsonResponse({
        'success': True,
        'room': room_data,
    })


def delete_room(request):
    if request.method == 'POST':
        room_id = request.POST.get('delete-room')
        room = Room.objects.get(id=room_id)
        room.delete()

    return redirect('index')


@login_required(login_url='login')
def update_profile(request):
    if request.method == 'POST':
       form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
       if form.is_valid():
           form.save()
           return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


def reply_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == "POST":
        reply_body = request.POST.get('reply')
        reply = Reply.objects.create(user=request.user, original_message=message, body=reply_body)
        message.replies.add(reply)

    return redirect('room', pk=message.room.id)
