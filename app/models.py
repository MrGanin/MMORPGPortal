from django.db import models
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField
from django.contrib.auth.forms import UserCreationForm

class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        return user

class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='Subscribe', related_name='posts')

    def __str__(self):
        return f'{self.title}'

class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)




class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory', related_name='categories')
    title = models.CharField(max_length = 50)
    text = models.TextField()



    def __str__(self):
        return f'{self.title} : {self.text} : {self.user}'

    def get_absolute_url(self):
        return f'/post/{self.id}'

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='images/')

class Movie(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    url = EmbedVideoField(null=True)

class Feedback(models.Model):
    accept = models.BooleanField(default=False)
    send_user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.text} : {self.send_user}'



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)




