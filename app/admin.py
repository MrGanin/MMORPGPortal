from django.contrib import admin
from .models import Post, Category, Feedback

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Feedback)
# Register your models here.
