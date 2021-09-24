import json
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import render  # RENDER() METHOD
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from chatterbot.trainers import ListTrainer
from .models import Botmessage, Userinput
from .budget.models import Budget


def index(request):
    return render(request, 'chatbot/app.html')

class ChatterBotAppView(TemplateView):
    template_name = 'chatbot/index.html'

    def get_context_data(self, **kwargs):
        botcontext = super().get_context_data(**kwargs)
        botcontext['botmessage'] = Botmessage.objects.all()
        return botcontext

    def get_context_data(self, **kwargs):
        usercontext = super().get_context_data(**kwargs)
        usercontext['userinput'] = Userinput.objects.all()
        return usercontext

    chatterbot = ChatBot(**settings.CHATTERBOT)

    trainer = ListTrainer(chatterbot)

    # Training with Personal Ques & Ans
    conversation = [
        "Hello", # user
        "Hi there", # bot
        "How are you", # user
        "I am doing great", # bot
        "That is good to hear", # user
        "Thank you", # bot
        "You are welcome", # user
        "Is there anything I can help you with", # bot
        "Yes please", # user
        "Is there anything I can help you with",  # bot
        "No thank you",  # user
        "Goodbye then, let's chat again soon", # bot
        "input gaby", # user
        "output gaby" # bot
    ]
    trainer.train(conversation)

    def post(self, request, *args, **kwargs):
        thisuser = request.user

        hotwords = [
            "date",
            "category",
            "details",
            "amount",
            "spend",
            "budget",
        ]

        # USERINPUT
        userText = request.POST.get('msg')
        print(userText)

        input_data = Userinput(userinput_text=userText, user=thisuser)
        input_data.save()

        # BOTMESSAGE
        botresp = self.chatterbot.get_response(userText)
        print(botresp)

        resp = Botmessage(botmessage_text=botresp, userinput_id=input_data.id, user=thisuser)
        resp.save()

        response_data = botresp.serialize()
        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        return render(request, 'chatbot/index.html')

class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    chatterbot = ChatBot(**settings.CHATTERBOT)

    # Training with Personal Ques & Ans
    conversation = [
        "Hello",
        "Hi there!",
        "How are you doing",
        "Im doing great",
        "That is good to hear",
        "Thank you",
        "You are welcome",
        "goodbye",
        "input gaby",
        "output gaby"
    ]

    trainer = ListTrainer(chatterbot)
    trainer.train(conversation)

    '''
    # Training with English Corpus Data
    trainer_corpus = ChatterBotCorpusTrainer(chatterbot)
    trainer_corpus.train(
        'chatterbot.corpus.english'
    )
    '''

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.
        * The JSON data should contain a 'text' attribute.
        """
        input_data = Userinput(userinput_text=json.loads(request.body.decode('utf-8')))
        input_data.save()

        print(input_data)

        '''
        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)
        '''

        print(json.loads(request.body.decode('utf-8')))

        response = self.chatterbot.get_response(json.loads(request.body.decode('utf-8')))
        print(response)

        resp = Botmessage(botmessage_text=response, userinput_id=input_data.id)
        resp.save()

        response_data = response.serialize()
        return JsonResponse(response_data, status=200)


    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return JsonResponse({
            'name': self.chatterbot.name
        })