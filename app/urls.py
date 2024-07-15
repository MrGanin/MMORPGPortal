from django.urls import path
from .views import (
    PostList, PostDetail, PostSearch, CreatePost, PostUpdate, PostDelete, IndexView,
    subscriber, unsubscriber, CreateFeedback, to_accept, misses, FeedbackUpdate
)



urlpatterns = [

    path('', PostList.as_view(), name='general'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='search'),
    path('create/', CreatePost.as_view(), name='post_create'),
    path('<int:pk>/feedback/', CreateFeedback.as_view(), name='feedback'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_edit'),
    path('<int:pk>/feedbackupdate/', FeedbackUpdate.as_view(), name='feedback_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('profile/', IndexView.as_view(), name='profile'),
    path('<int:pk>/toaccept/', to_accept, name='to_accept'),
    path('<int:pk>/misses/', misses, name='misses'),
    path('<int:pk>/subscribe/', subscriber, name='subscribe'),
    path('<int:pk>/unsubscribe/', unsubscriber, name='unsubscribe'),

]