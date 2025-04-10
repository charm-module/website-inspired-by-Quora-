from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.login_view, name='login'),  # new
    path('login/', views.login_view),                         # optional (redundant)
    path('logout/', views.logout_view, name='logout'),
    path('post-question/', views.post_question, name='post_question'),
    path('questions/', views.view_questions, name='view_questions'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    # path('like-answer/<int:answer_id>/', views.like_answer, name='like_answer'),
     path('like-answer/<int:answer_id>/', views.like_answer, name='like_answer'),
    #  path('delete-question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('delete-question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('react/<int:question_id>/', views.react_to_question, name='react_to_question'),



]

