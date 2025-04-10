from django import forms
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body']
        
from .models import Answer

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your answer...'})
        }
