
import json
import random
import requests
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from . import models

"""
The task question was little bit hard to understand. 
Things I did:
- This application can be used as a chatbot for telegram
- This application itself contains a route to chat to chatbot (like alternative for telegram)
- for both cases same response
- have a route to show availble calls to jokes and there counts with usernames
"""

def getjoke_response(message):
    """
    utility function returns response text
    """
    jokes = {
     'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
     'fat': ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
     'dumb': ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
                """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""] 
     }  

    if 'fat' in message['text']:
        return random.choice(jokes['fat'])
    
    elif 'stupid' in message['text']:
        return random.choice(jokes['stupid'])
    
    elif 'dumb' in message['text']:
        return random.choice(jokes['dumb'])

    elif message['text'] in ['hi', 'hey', 'hello']:
        return "Hello to you too! If you're interested in yo mama jokes, just tell me fat, stupid or dumb and i'll tell you an appropriate joke."
    else:
        return "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."
    
def save_counts(response_model, message):
    if(message == 'fat'):
        response_model.fat_count = response_model.fat_count + 1
    elif(message == 'dumb'):
        response_model.dumb_count = response_model.dumb_count + 1
    elif(message == 'stupid'):
        response_model.stupid_count = response_model.stupid_count + 1
    response_model.save()


class TelegramChatbot(generic.View):
    """
    This is the main view for handling telegram post request
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post_message_to_telegram(self, chat_id, text):
        url = f'https://api.telegram.org/bot{settings.TELEGRAMBOT_ID}/sendMessage?chat_id={chat_id}&text={text}'
        requests.post(url, headers={"Content-Type": "application/json"})
    
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        response_text = getjoke_response(incoming_message['message'])
        response_model, _ = models.ResponseCount.objects.get_or_create(
            source = models.ResponseCount.telegram,
            username = incoming_message['message']['from']['username']
        )
        save_counts(response_model, incoming_message['message']['text'])
        # if(incoming_message['message']['text'] == 'fat'):
        #     response_model.fat_count = response_model.fat_count + 1
        # elif(incoming_message['message']['text'] == 'dumb'):
        #     response_model.dumb_count = response_model.dumb_count + 1
        # elif(incoming_message['message']['text'] == 'stupid'):
        #     response_model.stupid_count = response_model.stupid_count + 1
        # response_model.save()
        self.post_message_to_telegram(incoming_message['message']['chat']['id'], response_text)
        return HttpResponse()


def webhooks(request):
    """

    """
    return render(request, 'main/webhooks.html',{})

@login_required
def chat(request):
    context = {}
    return render(request, 'main/chatbot.html', context)

def root_route(request):
    return render(request, 'main/root.html', {})

class ResponseCoutListView(generic.ListView):
    queryset = models.ResponseCount.objects.all()

# user views
class SigninView(auth_views.LoginView):
    def get_success_url(self):
        return reverse('chat')

class SignupView(generic.CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('signin')
