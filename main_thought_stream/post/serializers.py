from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    # This will serialize the replies for a given comment
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'parent_comment', 'created_at', 'replies']

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_comment=obj)
        return CommentSerializer(replies, many=True).data

    def create(self, validated_data):
        parent_comment = validated_data.get('parent_comment', None)
        comment = Comment.objects.create(**validated_data)
        return comment


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'content', 'image', 'created_at', 'updated_at', 'comments']
        read_only_fields = ['created_at', 'updated_at', 'author']  
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user  
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('author', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


        

