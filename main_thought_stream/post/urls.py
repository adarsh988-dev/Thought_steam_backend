from django.urls import path
from .views import PostView, PostCreationView, PostCommentsView, CommentView, PostUpdateDeleteView, CommentUpdateDeleteView

urlpatterns = [
    # Route for listing all posts (GET request)
    path('', PostView.as_view(), name='post-list'),

    # Route for creating a new post (POST request)
    path('create/', PostCreationView.as_view(), name='post-create'),

    # Route for listing comments of a specific post (GET request)
    path('<int:post_id>/comments/', PostCommentsView.as_view(), name='post-comments'),

    # Route for adding a comment to a specific post (POST request)
    path('<int:post_id>/comment/', CommentView.as_view(), name='post-comment-create'),

    # Route for updating or deleting a specific post (PUT or DELETE request)
    path('<int:post_id>/', PostUpdateDeleteView.as_view(), name='post-update-delete'),

    # Route for updating or deleting a specific comment (PUT or DELETE request)
    path('comment/<int:comment_id>/', CommentUpdateDeleteView.as_view(), name='comment-update-delete'),
]
