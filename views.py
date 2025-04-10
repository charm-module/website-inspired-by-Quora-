from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, redirect
from .models import Question
from .forms import QuestionForm
from django.contrib.auth.decorators import login_required

@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('view_questions')
    else:
        form = QuestionForm()
    return render(request, 'post_question.html', {'form': form})

def view_questions(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'view_questions.html', {'questions': questions})
from .models import Answer
from .forms import AnswerForm

def question_detail(request, question_id):
    question = Question.objects.get(id=question_id)
    answers = question.answers.all().order_by('-created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = AnswerForm(request.POST)
            if form.is_valid():
                answer = form.save(commit=False)
                answer.question = question
                answer.author = request.user
                answer.save()
                return redirect('question_detail', question_id=question.id)
        else:
            return redirect('login')
    else:
        form = AnswerForm()

    return render(request, 'question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form
    })

# from django.http import HttpResponseRedirect
# from django.urls import reverse

# @login_required
# def like_answer(request, answer_id):
#     answer = Answer.objects.get(id=answer_id)
    
#     if request.user != answer.author:  # optional: prevent liking own answer
#         if request.user in answer.liked_by.all():
#             answer.liked_by.remove(request.user)
#         else:
#             answer.liked_by.add(request.user)

#     return HttpResponseRedirect(reverse('question_detail', args=[answer.question.id]))


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Answer

@login_required
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)

    if request.user != answer.author:  # Optional: prevent liking own answer
        if request.user in answer.liked_by.all():
            answer.liked_by.remove(request.user)  # Unlike
        else:
            answer.liked_by.add(request.user)  # Like

    return HttpResponseRedirect(reverse('question_detail', args=[answer.question.id]))
from django.contrib import messages
from .models import Question

# @login_required
# def delete_question(request, question_id):
#     question = get_object_or_404(Question, id=question_id)

#     if question.author != request.user:
#         messages.error(request, "You are not allowed to delete this question.")
#         return redirect('view_questions')

#     if request.method == 'POST':
#         question.delete()
#         messages.success(request, "Question deleted successfully.")
#         return redirect('view_questions')

#     return render(request, 'confirm_delete.html', {'question': question})
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404, redirect, render
# from .models import Question

@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if question.author == request.user:
        if request.method == 'POST':
            question.delete()
            return redirect('view_questions')
    return redirect('view_questions')

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Question

@staff_member_required
def react_to_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        response = request.POST.get('admin_response')
        question.admin_response = response
        question.save()
        return redirect('view_questions')
    return render(request, 'react_to_question.html', {'question': question})
