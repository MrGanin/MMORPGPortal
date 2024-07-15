import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from .models import Post, Category, Subscribe, Image, Movie, Feedback
from .filters import PostFilter
from .forms import PostForm, FeedbackForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .tasks import send_message_on_email



class PostList(ListView):
    model = Post
    ordering = '-add_date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class PostDetail(DetailView, CreateView):
    form_class = FeedbackForm
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        a = Post.objects.filter(pk=self.object.pk).values('category')[0]
        context = super().get_context_data(**kwargs)
        context['id'] = self.object.category.values('pk')
        context['category'] = a['category']
        context['images'] = Image.objects.filter(post_id=self.object.pk)
        context['videos'] = Movie.objects.filter(post_id=self.object.pk)
        context['link_feedback'] = f'{self.object.pk}/feedback/'

        return context

    def post(self, request, *args, **kwargs):
        subscribers = Subscribe(
            user_id = request.user.pk,
            category_id = request.POST['category_id']
        )
        subscribers.save()

        return redirect('post_detail')




class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class CreatePost(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'createpost.html'

    def get_success_url(self):
        reverse_page = 'post_detail'
        return reverse_lazy(reverse_page, args=[self.object.pk])

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()

        for urlmov in [self.request.POST.get('movie1'), self.request.POST.get('movie2')]:
            Movie.objects.create(post_id=post.pk, url=urlmov)

        for i in self.request.FILES.getlist('images'):
            Image.objects.create(post_id=post.pk, file=i)

        return super().form_valid(form)

class CreateFeedback(LoginRequiredMixin, CreateView):
    form_class = FeedbackForm
    model = Feedback
    template_name = 'feedback.html'

    def form_valid(self, form):
        feedback = form.save(commit=False)
        feedback.send_user = self.request.user
        id = self.request.META['HTTP_REFERER'].split('/')[-3]
        feedback.post_id = id
        post = Post.objects.get(pk=id)
        send_message_on_email(user=post.user, post=post, title='Hовый отклик',
                              text=f'На ваш пост --> "{post.title}", получен новый отклик от пользователя \
                                  {self.request.user}. Текс отклика "{feedback.text}"'
                              )
        return super().form_valid(form)

    def get_success_url(self):
        reverse_page = 'post_detail'
        return reverse_lazy(reverse_page, args=[self.request.META['HTTP_REFERER'].split('/')[-3]])
class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'editpost.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objectpk'] = f'/posts/{self.object.pk}/update/'
        return context

class FeedbackUpdate(LoginRequiredMixin, UpdateView):
    form_class = FeedbackForm
    model = Feedback
    template_name = 'updatefeedback.html'

    def get_success_url(self):
        reverse_page = 'profile'
        return reverse_lazy(reverse_page)
class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'deletepost.html'
    success_url = reverse_lazy('general')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objectpk'] = f'/posts/{self.object.pk}/delete/'
        return context

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    model = Feedback

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.filter(user_id=self.request.user.pk)
        context['my_post_feedback'] = Feedback.objects.filter(post_id__in=post.values_list('pk', flat=True))
        return context

@login_required
def to_accept(request, pk):
    feedback = Feedback.objects.get(pk=pk)
    feedback.accept = True

    feedback.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def misses(request, pk):
    feedback = Feedback.objects.get(pk=pk)
    feedback.delete()
    return redirect(request.META.get('HTTP_REFERER'))



@login_required
def subscriber(request, pk):
    category = Category.objects.get(pk=pk)
    user = request.user
    category.subscribers.add(user)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscriber(request, pk):
    category = Category.objects.get(pk=pk)
    user = request.user
    category.subscribers.remove(user)
    return redirect(request.META.get('HTTP_REFERER'))

