from django.test import TestCase

# Create your tests here.

import datetime
from django.utils import timezone
from .models import Question

from django.urls import reverse

# Testing the Models. <DB>

class questionModelTest(TestCase):
    
    def test_recently_added_with_future_Quiz(self):
        future_Q= Question(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertIs(future_Q.recently_added(), False)
    
    # check for 1 ses older question
    def test_old_quiz_with_a_sec(self):
        old_quiz=Question(pub_date=timezone.now()-datetime.timedelta(days=1, seconds=1))
        self.assertIs(old_quiz.recently_added(), False)
        
    # Test a less than a second recent question
    def test_sec_earlier_quiz(self):
        less_sec_recent=Question(pub_date=timezone.now()-datetime.timedelta(hours=23, minutes=59, seconds=59, milliseconds=999))
        self.assertIs(less_sec_recent.recently_added(), True)
        
#fxn to create Question
def create_question(question_txt, days):
    
    dat=timezone.now()+ datetime.timedelta(days=days)
    return Question.objects.create(question_txt=question_txt, pub_date=dat)


#Run some tests on VIEWS

class testIndexView(TestCase):
    def test_no_question(self):
        # Test if there is no quiz present
        response =self.client.get(reverse("pollsite:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls Available")
        self.assertQuerysetEqual(response.context["latest_quiz_list"], [])
    
    
    #test an older question
    def test_older_quiz(self):
        question=create_question(question_txt="This is an old question", days=-31)
        response=self.client.get(reverse("pollsite:index"))
        self.assertQuerysetEqual(response.context['latest_quiz_list'], [question],)
    
    #test future question
    def test_future_question(self):
        question=create_question(question_txt="This is a future question", days=30)
        response=self.client.get(reverse("pollsite:index"))
        #not to be displayed
        self.assertContains(response, "No polls available")
        
        self.assertQuerysetEqual(response.context["latest_quiz_list"], [])
        
    #test both past and future quiz    
    def test_future_question_and_past_question(self):
        
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_txt="Past question.", days=-30)
        create_question(question_txt="Future question.", days=30)
        response = self.client.get(reverse("pollsite:index"))
        
        self.assertQuerysetEqual(
            response.context["latest_quiz_list"],
            [question],
        )

    # two past questions
    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_txt="Past question 1.", days=-30)
        question2 = create_question(question_txt="Past question 2.", days=-5)
        response = self.client.get(reverse("pollsite:index"))
        self.assertQuerysetEqual(
            response.context["latest_quiz_list"],
            [question2, question1],
        )
        
#Testing the Detail View

class testDetailsView(TestCase):
    
    #test future question
    def test_future_question(self):
        question=create_question(question_txt="This a future question", days=10)
        url=reverse("pollsite:detail", args=(question.id,))
        response=self.client.get(url)
        self.assertEqual(response.status_code, 404)
       
    #test past quiz 
    def test_past_quiz(self):
        question=create_question(question_txt="This is a past question", days= -49)
        response=self.client.get(reverse("pollsite:detail", args=question.id))
        self.assertContains(response, question.question_txt)