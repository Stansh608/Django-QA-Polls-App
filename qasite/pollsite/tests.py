from django.test import TestCase

# Create your tests here.

import datetime
from django.utils import timezone
from .models import Question


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