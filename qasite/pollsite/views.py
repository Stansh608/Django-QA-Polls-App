from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import F

# import the models
from .models import Question, Answer


# Create your views here.

#Using generic views
class IndexView(generic.ListView):
    template_name="pollsite/index.html"
    context_object_name= "latest_quiz_list"
    
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')
    
    
#details of the Question
class DetailView(generic.DetailView):
    model=Question
    template_name="pollsite/detail.html"
    

# vote Action
def Vote(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    try:
        selected_ans=question.answer_set.get(pk=request.POST['ans'])
    except(KeyError, Answer.DoesNotExist):
        return render(
            request,
            "pollsite/detail.html",
            {
                "question": question,
                "error_message": "You did not select an Answer",
            }
        )
        
    selected_ans.votes=F('votes') + 1
    selected_ans.save()
    return HttpResponseRedirect(reverse("pollsite:results", args=(question.id,))) # Redirect to results page 
        

#Results
class ResultsView(generic.DetailView):
    model= Question
    template_name= "pollsite/result.html"
    