# friends/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import RegisterForm, FriendForm
from .models import Friend, Profile
import uuid
from datetime import date, timedelta

def index_view(request):
    return render(request, 'friends/index.html')

def about_view(request):
    return render(request, 'friends/about.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('friend_list')
    else:
        form = RegisterForm()
    return render(request, 'friends/register.html', {'form': form})

@login_required
def friend_list_view(request):
    friends = Friend.objects.filter(profile=request.user.profile)

    today = date.today()
    tomorrow = today + timedelta(days=1)

    friends_today = []
    friends_tomorrow = []
    other_friends = []

    for friend in friends:
        if friend.birthday.month == today.month and friend.birthday.day == today.day:
            friends_today.append(friend)
        elif friend.birthday.month == tomorrow.month and friend.birthday.day == tomorrow.day:
            friends_tomorrow.append(friend)
        else:
            other_friends.append(friend)

    context = {
        'friends_today': friends_today,
        'friends_tomorrow': friends_tomorrow,
        'other_friends': other_friends,
    }
    return render(request, 'friends/friend_list.html', context)

@login_required
def add_friend_view(request):
    if request.method == 'POST':
        form = FriendForm(request.POST)
        if form.is_valid():
            friend = form.save(commit=False)
            friend.profile = request.user.profile
            friend.save()
            return redirect('friend_list')
    else:
        form = FriendForm()
    return render(request, 'friends/add_friend.html', {'form': form})

@login_required
def edit_friend_view(request, friend_id):
    friend = get_object_or_404(Friend, id=friend_id, profile=request.user.profile)
    if request.method == 'POST':
        form = FriendForm(request.POST, instance=friend)
        if form.is_valid():
            form.save()
            return redirect('friend_list')
    else:
        form = FriendForm(instance=friend)
    return render(request, 'friends/edit_friend.html', {'form': form})

@login_required
def delete_friend_view(request, friend_id):
    friend = get_object_or_404(Friend, id=friend_id, profile=request.user.profile)
    if request.method == 'POST':
        friend.delete()
        return redirect('friend_list')
    return render(request, 'friends/delete_friend.html', {'friend': friend})

@login_required
def telegram_link_view(request):
    profile = request.user.profile
    return render(request, 'friends/telegram_link.html', {'profile': profile})

@login_required
def generate_new_code_view(request):
    profile = request.user.profile
    profile.telegram_code = uuid.uuid4().hex[:16]
    profile.save()
    return redirect('telegram_link')

@login_required
def unlink_telegram_view(request):
    profile = request.user.profile
    profile.telegram_id = None
    profile.save()
    return redirect('telegram_link')