from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core import serializers  # JSON SERIALIZE METHOD
from django.template import loader   # TEMPLATE METHOD
from django.shortcuts import render  # RENDER() METHOD
from django.urls import reverse

from .models import Question, Choice

def index(request):
    return HttpResponse("Hello, you're at the polls index.")

def list_questions(request):
    questions = Question.objects.all()

    # JSON SERIALIZE METHOD questions_json = serializers.serialize('json', questions) # alternative to render in json
    # JSON SERIALIZE METHOD return HttpResponse(questions_json)

    # TEMPLATE METHOD template = loader.get_template('polls/index.html')
    # TEMPLATE METHOD context = {
    # TEMPLATE METHOD     'questions': questions,
    # TEMPLATE METHOD }
    # TEMPLATE METHOD return HttpResponse(template.render(context, request))

    # RENDER() METHOD
    context = {'questions': questions}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    # return HttpResponse("You're looking at question %s." % question_id)

    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/details.html', {'question': question})

def vote(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    try:
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'polls/details.html', {
            'question': question,
            'error_message': "You didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # always return an HttpResponseRedirect after successfully dealing with POST data as this prevents data from being posted twice if user hits Back button
        return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))