from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from django.db.models import Count
from rest_framework import generics, status
from rest_framework.response import Response
from accounts.serializers import UserSerializer, FollowSerializer, PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.exceptions import NotFound, ValidationError
from accounts.models import CustomUser, Follow, Post, Comment, Like
from rest_framework import generics
from .serializers import BotSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import F


class BotRegistrationAPIView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = BotSerializer

class CreatePostAPIView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        title = request.data.get("title")
        content = request.data.get("content")
        user = get_object_or_404(CustomUser, id=user_id)
        post = Post.objects.create(author=user, title=title, content=content)
        return Response({"Success": f"Post created."}, status=status.HTTP_201_CREATED)


class GetPostsAPIView(generics.ListAPIView):
    permission_classes = []
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        return queryset
    
    
class GetFollowedPostsAPIView(generics.ListAPIView):
    permission_classes = []
    serializer_class = FollowSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        user = get_object_or_404(CustomUser, id=user_id)
        followed_users = Follow.objects.filter(follower=user)
        queryset = Post.objects.filter(author__in=followed_users.values('following__username'))
        return queryset


class FollowUserAPIView(APIView):
    permission_classes = []
    serializer_class = FollowSerializer

    def post(self, request, *args, **kwargs):
        follower = request.data.get("follower")
        followed = request.data.get("followed")

        follower_user = get_object_or_404(CustomUser, id=follower)
        followed_user = get_object_or_404(CustomUser, id=followed)

        followed, created = Follow.objects.get_or_create(
            follower=follower_user, followed=followed_user)
        
        if created:
            followed_user.followers_count = F('followers_count') + 1
            followed_user.save()
            print(followed_user.followers_count)
            return Response({
                            "Success": f"User {followed_user.username} followed."}, status=status.HTTP_201_CREATED)
        else:
            followed.delete()
            followed_user.followers_count = F('followers_count') - 1
            followed_user.save()
            print(followed_user.followers_count)
            return Response({
                            "Success": f"User {followed_user.username} unfollowed.",
                            }, status=status.HTTP_202_ACCEPTED)



class GetFollowedPostsAPIView(generics.ListAPIView):
    permission_classes = []
    serializer_class = PostSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        user = get_object_or_404(CustomUser, id=user_id)
        followed_users = Follow.objects.filter(follower=user)
        queryset = Post.objects.filter(author__in=followed_users.values_list('followed', flat=True))
        return queryset
    

class LikePostsAPIView(APIView):
    permission_classes = []
    serializer_class = PostSerializer
    
    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        post_id = request.data.get("post_id")
        user = get_object_or_404(CustomUser, id=user_id)
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=user, post=post)

        if created:
            post.likes = F('likes') + 1
            response_message = f"Post {post.title} liked."
        else:
            like.delete()
            post.likes = F('likes') - 1
            response_message = f"Post {post.title} unliked."

        post.save()

        return Response({"Success": response_message}, status=status.HTTP_201_CREATED if created else status.HTTP_202_ACCEPTED)


class CreateCommentAPIView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        post_id = request.data.get("post_id")
        content = request.data.get("content")

        post = get_object_or_404(Post, id=post_id)
        user = get_object_or_404(CustomUser, id=user_id)

        comment = Comment.objects.create(
            author=user, post=post, content=content)
        return Response({"Success": f"Comment created."}, status=status.HTTP_201_CREATED)


class GetUserProfileAPIView(generics.ListAPIView):
    permission_classes = []
    serializer_class = UserSerializer

    def get_queryset(self):
        username = self.kwargs.get("user")
        print(username)
        queryset = CustomUser.objects.filter(username=username)
        return queryset        
    

class GetSuggestedPostsAPIView(generics.ListAPIView):
    permission_classes = []
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all().annotate(likes_count=F('likes') - F('likes_relation__id'))
        return queryset
    
class GetSuggestedUsersAPIView(generics.ListAPIView):
    permission_classes = []
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = CustomUser.objects.all().exclude(username=self.request.user.username).order_by('-followers_count')[:20]
        return queryset
    

class GetUsersAPIView(generics.ListAPIView):
    permission_classes = []
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        return queryset

class CreateCommentAPIView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        post_id = request.data.get("post_id")
        content = request.data.get("content")
        user = get_object_or_404(CustomUser, id=user_id)
        post = get_object_or_404(Post, id=post_id)
        comment = Comment.objects.create(
            author=user, post=post, content=content)
        return Response({"Success": f"Comment created."}, status=status.HTTP_201_CREATED)


class GetCommentAPIView(ListAPIView):
    permission_classes = []
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        comment_id = self.kwargs.get("comment_id")
        try:
            comment = Comment.objects.get(id=comment_id)
            serializer = Comment(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            raise NotFound(detail="Comment not found", code=404)
        except ValidationError:
            raise NotFound(detail="Comment not found", code=404)


class GetBotAPIView(generics.ListAPIView):
    permission_classes = []
    serializer_class = BotSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        queryset = CustomUser.objects.filter(id=user_id)
        return queryset


class DeleteCommentAPIView(DestroyAPIView):
    permission_classes = []
    serializer_class = CommentSerializer


    def get_queryset(self):
        comment_id = self.kwargs.get("pk")
        print(comment_id)
        return Comment.objects.filter(id=comment_id)

    
class ChangeCommentAPIView(UpdateAPIView):
    permission_classes = []
    serializer_class = CommentSerializer

    def get_queryset(self):
        comment_id = self.kwargs.get("comment_id")
        return Comment.objects.filter(id=comment_id)

            