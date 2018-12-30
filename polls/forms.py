from django import forms

from .models import Question, Choice

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('question_text',)

class ChoiceForms(forms.ModelForm):

    class Meta:
        model = Choice
        fields = ('question', 'choice_text')
