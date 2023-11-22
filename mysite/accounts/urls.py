# urls.py
from django.urls import path
from .views import (UserRegistrationAPIView, 
                    UserLoginAPIView, 
                    FollowUserAPIView, 
                    CreatePostAPIView, 
                    GetPostsAPIView, 
                    GetFollowedPostsAPIView, 
                    LikePostsAPIView, 
                    GetUserProfileAPIView,
                    CreateCommentAPIView,
                    GetSuggestedPostsAPIView,
                    GetSuggestedUsersAPIView,
                    getUsersAPIView
                    )

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="register"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("create_post/", CreatePostAPIView.as_view(), name="create_post"),
    path("get_posts/<int:user_id>/", GetPostsAPIView.as_view(), name="get_posts"),
    path("get_followed_posts/", GetFollowedPostsAPIView.as_view(), name="get_posts"),
    path("comment/", CreateCommentAPIView.as_view(), name="create_comment"),
    path("like/", LikePostsAPIView.as_view(), name="like_posts"),
    path("follow/", FollowUserAPIView.as_view(), name="follow_user"),
    path("suggested_posts/", GetSuggestedPostsAPIView.as_view(), name="suggested_posts"),
    path("suggested_profiles/", GetSuggestedUsersAPIView.as_view(), name="suggested_profiles"),

        
    ### checking ###
    ### string parameter ###
    path("profile/<int:user_id>/", GetUserProfileAPIView.as_view(), name="get_profile"),
    path("users", getUsersAPIView.as_view(), name="get_profile"),



    ### Bot urls ###
]
