# serializers.py
from .models import Follow, Post, Like, CustomUser, Comment
from rest_framework import serializers



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ("id", "author", 'content', 'created_at',)


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ("id", "author", 'title', 'content', "comments", 'likes', 'created_at',)

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ("id", 'follower', 'followed', 'created_at',)


class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', "posts", "is_bot", 'followers_count', 'created_at',)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    

class BotSerializer(serializers.ModelSerializer):
    is_bot = serializers.BooleanField(default=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', "is_bot", 'followers_count', 'created_at',)
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user




class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", 'user', 'post', 'created_at',)
