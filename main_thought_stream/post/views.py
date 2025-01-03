from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly,AllowAny
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment
from .authentication import CustomJWTAuthentication

class PostView(APIView):
    permission_classes = []
    authentication_classes = [] 

    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
class PostCreationView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    
    def post(self, request):
        print("request--->",request.user)
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class PostCommentsView(generics.ListAPIView):
    permission_classes = [AllowAny] 
    authentication_classes = []  
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        Override to filter comments by post_id from the URL.
        """
        post_id = self.kwargs.get('post_id')
        print("post id is----->",post_id)
        try:
            post = Post.objects.get(id=post_id)  
        except Post.DoesNotExist:
            return Comment.objects.none() 

        return Comment.objects.filter(post=post_id, parent_comment__isnull=True).order_by('created_at')

class CommentView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided or are invalid.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        print("request",request.data)
        content = request.data.get('content')
        parent_comment_id = request.data.get('parent_comment',None)

        # Check if parent_comment_id is provided and exists
        parent_comment = None
        if parent_comment_id:
            try:
                parent_comment = Comment.objects.get(id=parent_comment_id)
            except Comment.DoesNotExist:
                return Response({'detail': 'Parent comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Prepare data for the new comment
        data = {
            'post': post.id,
            'content': content,
            'user': request.user.id,
            'parent_comment': parent_comment.id if parent_comment else None
        }

        serializer = CommentSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostUpdateDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the authenticated user is the author of the post
        if post.author != request.user:
            return Response({'detail': 'You do not have permission to edit this post.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Serialize and update the post
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # Save the changes
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method to delete an existing post
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the authenticated user is the author of the post
        if post.author != request.user:
            return Response({'detail': 'You do not have permission to delete this post.'},
                            status=status.HTTP_403_FORBIDDEN)

        post.delete()  # Delete the post
        return Response({'detail': 'Post deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class CommentUpdateDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    # PUT method to update an existing comment
    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'detail': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the authenticated user is the author of the comment
        if comment.user != request.user:
            return Response({'detail': 'You do not have permission to edit this comment.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Serialize and update the comment
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method to delete an existing comment
    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'detail': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the authenticated user is the author of the comment
        if comment.user != request.user:
            return Response({'detail': 'You do not have permission to delete this comment.'},
                            status=status.HTTP_403_FORBIDDEN)

        comment.delete()  # Delete the comment
        return Response({'detail': 'Comment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
