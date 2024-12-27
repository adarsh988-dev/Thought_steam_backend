from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'parent_comment','created_at']

        
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image','created_at', 'updated_at','comments']
        read_only_fields = ['created_at', 'updated_at'] 

    def create(self, validate_data):
        user = self.context['request'].user  
        validate_data['author'] = user  
        return super().create(validate_data)
    
    def update(self, instance, validated_data):
        # Ensure the 'author' is not updated
        validated_data.pop('author', None)  

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

        

