from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.utils import timezone


class IndexView(ListView):
    template_name = 'voting_app/index.html'
    context_object_name = 'list_of_questions'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date').\
            exclude(choice__question__isnull=True)


class DetailsView(DetailView):
    model = Question
    template_name = 'voting_app/details.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(DetailsView):
    model = Question
    template_name = 'voting_app/results.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):

        return render(request, 'voting_app/details.html', {
            'question': question,
            'error_message': "You haven't made any choice!",
        })
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('voting_app:results', args=(question.id,)))








