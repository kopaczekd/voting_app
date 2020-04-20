from django.test import TestCase
from .models import Question, Choice
import datetime
from django.utils import timezone
from django.urls import reverse


# Testing model 'Question' (is_recent method)
class QuestionModelTests(TestCase):

    def test_is_recent_in_the_future(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_recent(), False)

    def test_is_recent_now(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=58)
        present_question = Question(pub_date=time)
        self.assertIs(present_question.is_recent(), True)

    def test_is_recent_in_past(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=20)
        past_question = Question(pub_date=time)
        self.assertIs(past_question.is_recent(), False)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days)
    return Question.objects.create(question_text=question_text, pub_date=time)


def create_choice(question, choice_text):
    return Choice.objects.create(question=question, choice_text=choice_text)


# Testing IndexView, that he is work properly with future questions, past questions and no questions.
class IndexViewTests(TestCase):

    def test_no_questions(self):
        response = self.client.get(reverse('voting_app:index'))
        self.assertContains(response, 'There is no questions!')
        self.assertQuerysetEqual(response.context['list_of_questions'], [])
        self.assertEqual(response.status_code, 200)

    def test_present_questions(self):
        question1 = create_question('Present question', 0)
        create_choice(question1, 'Choice 1')
        response = self.client.get(reverse('voting_app:index'))
        print(f"Query set: {response.context['list_of_questions']}")
        self.assertQuerysetEqual(response.context['list_of_questions'], ['<Question: Present question>'])

    def test_past_questions(self):
        question1 = create_question('Past questions', -10)
        create_choice(question1, 'Choice 1')
        response = self.client.get(reverse('voting_app:index'))
        self.assertQuerysetEqual(response.context['list_of_questions'], ['<Question: Past questions>'])

    def test_future_questions(self):
        create_question('Future questions', 2)
        response = self.client.get(reverse('voting_app:index'))
        self.assertQuerysetEqual(response.context['list_of_questions'], [])

    def test_future_and_past_questions_together_with_choices(self):
        question1 = create_question('Past questions', -10)
        question2 = create_question('Future question', 10)
        create_choice(question1, 'Choice 1')
        create_choice(question2, 'Choice 2')
        response = self.client.get(reverse('voting_app:index'))
        self.assertQuerysetEqual(response.context['list_of_questions'], ['<Question: Past questions>'])

    def test_a_few_past_questions(self):
        question1 = create_question('Past question 1', -8)
        question2 = create_question('Past question 2', -9)
        question3 = create_question('Past question 3', -20)
        create_choice(question1, 'Choice 1')
        create_choice(question2, 'Choice 2')
        create_choice(question3, 'Choice 3')
        response = self.client.get(reverse('voting_app:index'))
        self.assertQuerysetEqual(response.context['list_of_questions'], ['<Question: Past question 1>',
                                                                         '<Question: Past question 2>',
                                                                         '<Question: Past question 3>'])

    def test_question_without_choices(self):
        create_question('Question without choice', -2)
        response = self.client.get(reverse('voting_app:index'))
        self.assertQuerysetEqual(response.context['list_of_questions'], [])

    def test_question_with_one_choice(self):
        create_question('Question without choice', -2)
        question2 = create_question('Question with one choice', -3)
        create_choice(question2, 'Choice 1')
        response = self.client.get(reverse('voting_app:index'))
        self.assertQuerysetEqual(response.context['list_of_questions'], ['<Question: Question with one choice>'])

    def test_question_with_few_choices(self):
        question1 = create_question('Correct created question', -2)
        create_choice(question1, 'Choice 1')
        create_choice(question1, 'Choice 2')
        response = self.client.get(reverse('voting_app:index'))
        self.assertQuerysetEqual(response.context['list_of_questions'], ['<Question: Correct created question>'])




