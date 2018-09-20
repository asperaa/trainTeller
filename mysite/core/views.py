from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from dialogflow_lite.dialogflow import Dialogflow

import json
import requests

from mysite.core.forms import SignUpForm
from mysite.core.forms import ChatForm
from .models import Profile

myapikey='rfgbncxndq'

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

            if(len(mess.response.split())!=2):
                mess.save()

                return render(request, 'chat.html', {'mess': mess})

            else:
                source, destination = mess.response.split()
                source_code_response = requests.get('https://api.railwayapi.com/v2/name-to-code/station/'+source+'/apikey/rfgbncxndq/')
                dest_code_response = requests.get('https://api.railwayapi.com/v2/name-to-code/station/'+destination+'/apikey/rfgbncxndq/')

                source_code_json = source_code_response.json()
                dest_code_json = dest_code_response.json()


                source_code = source_code_json["stations"][0]["code"]
                dest_code = dest_code_json["stations"][0]["code"]


                final_response = requests.get('https://api.railwayapi.com/v2/between/source/'+source_code+'/dest/'+dest_code+'/date/<15-09-2018>/apikey/rfgbncxndq/')
                final_response_json = final_response.json()
                final_response_string = json.dumps(final_response_json)
                mess.response = final_response_string
                mess.save()

                return render(request, 'chat.html', {'mess': mess})

    else:
        form = ChatForm()

    return render(request, 'sendMessage.html', {'form': form})


