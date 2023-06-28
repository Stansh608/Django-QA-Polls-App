from django.db import models
from django.utils import timezone
import datetime
# Create your models here.

class Question(models.Model):
    question_txt=models.CharField(("Question Text"), max_length=500) # Question Text will be the label on Django admin site once this model is registered
    pub_date=models.DateTimeField(("Date Published"))
    
    def __str__(self):
        return self.question_txt
    
    def recently_added(self):
        now=timezone.now()
        return now - datetime.timedelta(days=1) <=self.pub_date <= now #this takes the current time and subtracts a day. Then compares whether the question
                                                                            #has been posted from that time to recent.
                                                                            
class Answer(models.Model):
    question=models.ForeignKey(Question, on_delete=models.CASCADE) # Relationship, association
    answer_txt=models.CharField(max_length=100)
    votes=models.IntegerField(default=0)
    
    def __str__(self):
        return self.answer_txt # Once the answer is added, return its txt