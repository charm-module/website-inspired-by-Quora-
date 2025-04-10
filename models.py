from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # New field for admin response
    admin_response = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    
from django.contrib.auth.models import User

class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name='liked_answers', blank=True)  # ✅ Like system

    def like_count(self):
        return self.liked_by.count()

    def __str__(self):
        return f'Answer by {self.author.username}'


