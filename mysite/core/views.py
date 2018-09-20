from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from dialogflow_lite.dialogflow import Dialogflow

import json

from mysite.core.forms import SignUpForm
from mysite.core.forms import ChatForm
from .models import Profile


@login_required
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            #user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def chat(request):

    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            mess = form.save(commit=False)
            user_uid = Profile.objects.get(user=request.user)
            mess.user_uuid = user_uid
            dialogflow = Dialogflow(**settings.DIALOGFLOW)
            responses = dialogflow.text_request(str(mess.message))
            mess.response = responses[0]

            mess.save()

            return render(request, 'chat.html', {'mess': mess})
    else:
        form = ChatForm()

    return render(request, 'sendMessage.html', {'form': form})


