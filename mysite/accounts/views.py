from rest_framework.authentication import TokenAuthentication
from .models import Follow, Post, Like, CustomUser, Comment
from rest_framework import generics
from .serializers import UserSerializer, BotSerializer, FollowSerializer, PostSerializer, CommentSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
# import f to increment followers count
from django.db.models import F


class UserRegistrationAPIView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = UserSerializer


class UserLoginAPIView(APIView):
    permission_classes = []
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = get_object_or_404(CustomUser, username=username)
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id, 'username': user.username}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class CreatePostAPIView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GetPostsAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        return queryset
    
class GetFollowedPostsAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def get_queryset(self):
        followed_users = Follow.objects.filter(follower=self.request.user)
        queryset = Post.objects.filter(author__in=followed_users.values('following__username'))
        return queryset


class FollowUserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("followed")
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        followed, created = Follow.objects.get_or_create(
            follower=request.user, followed=user_to_follow)
        if created:
            user_to_follow.followers_count = F('followers_count') + 1
            user_to_follow.save()
            print(user_to_follow.followers_count)
            return Response({
                            "Success": f"User {user_to_follow.username} followed."}, status=status.HTTP_201_CREATED)
        else:
            followed.delete()
            user_to_follow.followers_count = F('followers_count') - 1
            user_to_follow.save()
            print(user_to_follow.followers_count)
            return Response({
                            "Success": f"User {user_to_follow.username} unfollowed.",
                            }, status=status.HTTP_202_ACCEPTED)


class GetFollowedPostsAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        followed_users = Follow.objects.filter(follower=self.request.user)
        queryset = Post.objects.filter(author__in=followed_users.values_list('followed', flat=True))
        return queryset
    

class LikePostsAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    
    def post(self, request, *args, **kwargs):
        post_id = request.data.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        post_id = request.data.get("post_id")
        content = request.data.get("content")
        post = get_object_or_404(Post, id=post_id)
        comment = Comment.objects.create(
            author=request.user, post=post, content=content)
        return Response({"Success": f"Comment created."}, status=status.HTTP_201_CREATED)


class GetUserProfileAPIView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        user_id = self.kwargs.get("user_id")
        return CustomUser.objects.filter(id=user_id).first()
    

class GetSuggestedPostsAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all().annotate(likes_count=F('likes') - F('likes_relation__id'))
        return queryset
    
    
class GetSuggestedUsersAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = CustomUser.objects.all().exclude(username=self.request.user.username).order_by('-followers_count')[:20]
        return queryset


class getUsersAPIView(generics.ListAPIView):
    permission_classes = []
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        return queryset