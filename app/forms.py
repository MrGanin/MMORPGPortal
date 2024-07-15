from django import forms

from .models import Post, Feedback
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result



class PostForm(forms.ModelForm):
    movie1 = forms.URLField(label='Вставьте ссылку на видео №1', required=False)
    movie2 = forms.URLField(label='Вставьте ссылку на видео №2', required=False)
    images = MultipleFileField(label='Выберите изображения', required=False)


    class Meta:
        model = Post
        fields = ['title', 'text', 'category']
        labels = {
            'title' : 'Введите заголовок',
            'text' : 'Напишите текст поста',
            'category' : 'Выберите категорию'

        }
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['text']
        labels = {
            'text' : 'Текст отклика'
        }