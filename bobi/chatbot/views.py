import datetime
import json

from django.db.models import Sum
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
    ]
    trainer.train(conversation)

    trainer.train([
        "I spent money", # user
        "Please tell me in this format: category XX details XX amount XX", # bot
        "category XX details XX amount XX", # user
        "I have recorded your spending as requested. Please proceed to /budget to view your records.", # bot
    ])

    trainer.train([
        "Destroy entry",  # user
        "Please tell me the id of the entry you would like to delete",  # bot
        "Destroy entry id",  # user
        "I have destroyed your entry as requested. Please proceed to /budget to view your records.",  # bot
    ])

    trainer.train([
        "Spending insights",  # user
        "What would you like to find out about your spending?",  # bot
        "How much did I spend in",  # user
        "Look in your console to see the results.",  # bot
    ])

    trainer.train([
        "Spending insights",  # user
        "What would you like to find out about your spending?",  # bot
        "How much did I spend on",  # user
        "Look in your console to see the results.",  # bot
    ])

    budgetconvo = [
        "I spent money",  # user
        "Please tell me in this format: category XX details XX amount XX",  # bot
        "category" and "details" and "amount",  # user
        "I have recorded your spending as requested. Please proceed to /budget to view your records.",  # bot
    ]
    trainer.train(budgetconvo)

    def post(self, request, *args, **kwargs):
        thisuser = request.user

        # USERINPUT
        userText = request.POST.get('msg')
        print(userText)

        input_data = Userinput(userinput_text=userText, user=thisuser)
        input_data.save()

        if "category" and "details" and "amount" in userText:
            # save budget records
            # userinput format is "category EXAMPLE details EXAMPLE amount EXAMPLE"
            listofusertext = userText.split()
            category = listofusertext[1].lower()
            details = listofusertext[3].lower()
            amount = float(listofusertext[5])

            spendentry = Budget(category=category, details=details, amount=amount, user=thisuser)
            spendentry.save()

            # generate bot response and save to botmessage db
            botresp = self.chatterbot.get_response(userText)
            print(botresp)

            resp = Botmessage(botmessage_text=botresp, userinput_id=input_data.id, user=thisuser)
            resp.save()

            response_data = botresp.serialize()
            return JsonResponse(response_data, status=200)
        elif "how much" and "spend" in userText:
            listofusertext = userText.split()
            factor = listofusertext[5]

            # how much did I spend IN month
            if factor == 'in':
                monthstr = listofusertext[6]
                print(monthstr)
                monthint = datetime.datetime.strptime(monthstr, "%B").month
                print(monthint)

                recordstosummate = Budget.objects.all().filter(date__month=monthint).values()
                print(recordstosummate)

                sum = 0
                for x in recordstosummate:
                    sum = sum + float(x["amount"])
                print(sum)
            # how much did I spend ON category
            elif factor == 'on':
                category = listofusertext[6]
                print(category)

                recordstosummate = Budget.objects.all().filter(category=category).values()
                print(recordstosummate)

                sum = 0
                for x in recordstosummate:
                    sum = sum + float(x["amount"])
                print(sum)

            botresp = self.chatterbot.get_response(userText)
            print(botresp)

            resp = Botmessage(botmessage_text=botresp, userinput_id=input_data.id, user=thisuser)
            resp.save()

            response_data = botresp.serialize()
            return JsonResponse(response_data, status=200)
        elif "Destroy entry id" in userText:
            # userinput format is "destroy entry id XXX"
            listofusertext = userText.split()
            id = int(listofusertext[3])

            if id:
                recordtodestroy = Budget.objects.filter(id=id)
                recordtodestroy.delete()

                # BOTMESSAGE
                botresp = self.chatterbot.get_response(userText)
                print(botresp)

                resp = Botmessage(botmessage_text=botresp, userinput_id=input_data.id, user=thisuser)
                resp.save()

                response_data = botresp.serialize()
                return JsonResponse(response_data, status=200)
            else:
                botresp = self.chatterbot.get_response(userText)
                print(botresp)

                resp = Botmessage(botmessage_text=botresp, userinput_id=input_data.id, user=thisuser)
                resp.save()

                response_data = botresp.serialize()
                return JsonResponse(response_data, status=200)
        else:
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
