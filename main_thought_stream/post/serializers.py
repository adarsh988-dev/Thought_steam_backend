from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username'] 


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'parent_comment', 'created_at', 'replies']

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_comment=obj).order_by('created_at')
        return CommentSerializer(replies, many=True).data

    def create(self, validated_data):
        parent_comment = validated_data.get('parent_comment', None)
        comment = Comment.objects.create(**validated_data)
        return comment


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'content', 'image', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'author']


    def create(self, validated_data):
        user = self.context['request'].user
        print("-------------->",user.id)
        validated_data['author'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('author', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
