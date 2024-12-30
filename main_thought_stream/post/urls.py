from django.urls import path
from .views import PostView, CommentView

urlpatterns = [
    path('', PostView.as_view(), name='post-list'),  
    path('<int:pk>/', PostView.as_view(), name='post-detail'),
    path('comments/', CommentView.as_view(), name='comment-create'), 
    ]
