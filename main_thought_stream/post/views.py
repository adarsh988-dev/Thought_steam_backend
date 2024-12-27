from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer, CommentSerializer
from .models import Post

class PostView(APIView):
    permission_classes = [IsAuthenticated]
    
    # GET method to retrieve all posts with their comments
    def get(self, request):
        posts = Post.objects.all()
        # Use the PostSerializer to serialize the posts along with their related comments
        serializer = PostSerializer(posts, many=True)
        print(serializer.data)
        return Response(serializer.data)

    # POST method to create a new post
    def post(self, request):
        print("request data ---->",request.user)
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided or are invalid.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # PUT method to update an existing post
    def put(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the authenticated user is the author of the post
        if post.author != request.user:
            return Response({'detail': 'You do not have permission to edit this post.'},
                            status=status.HTTP_403_FORBIDDEN)
        
        # Use the PostSerializer to validate and update the post
        serializer = PostSerializer(post, data=request.data, partial=True)  # Partial update allows updating specific fields
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # Save the changes
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method to delete a post
    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the current user is the author of the post
        if post.author != request.user:
            return Response({'detail': 'You do not have permission to delete this post.'},
                            status=status.HTTP_403_FORBIDDEN)
        
        post.delete() 
        return Response({'detail': 'Post deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    # POST method to create a new comment
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided or are invalid.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Save the comment, associating it with the authenticated user
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
