from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .forms import QuestionForm, ChoiceForm
from .models import Question, Choice

# Create your views here.


def post(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
    #        post.author = request.user
            post.pub_date = timezone.now()
            post.save()
            return redirect('polls:detail', pk=post.pk)
    else:
        form = QuestionForm()
#    path('<int:pk>/', views.DetailView.as_view(), name='detail'),

    return render(request, 'polls/question_edit.html', {'form': form})

def add_choice(request, pk):
    if request.method == "POST":
        form = ChoiceForm(request.POST)
        question = get_object_or_404(Question, pk=pk)

        if form.is_valid():
            post = form.save(commit=False)
    #        post.author = request.user
            post.question = form.cleaned_data['question']
            post.votes = 0
    #        post.rating = 0
            post.save()
            return redirect('polls:detail', pk=post.question.pk)
    else:
        form = ChoiceForm()
#    path('<int:pk>/', views.DetailView.as_view(), name='detail'),

    return render(request, 'polls/choice_edit.html', {'form': form})

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def post_edit(request, pk):
    post = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
    #        post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('polls:detail', pk=post.id)
    else:
        form = QuestionForm(instance=post)
    return render(request, 'polls/question_edit.html', {'form': form})

def edit_choice(request, pk):
    post = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = ChoiceForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
    #        post.author = request.user
            post.question = question.choice_set.get(pk=request.POST['choice'])
            post.votes = 0
            post.save()
            return redirect('polls:detail', pk=post.id)
    else:
        form = ChoiceForm(instance=post)
    return render(request, 'polls/choice_edit.html', {'form': form})
