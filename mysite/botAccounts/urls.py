from django.urls import path
from .views import BotRegistrationAPIView, CreatePostAPIView, GetPostsAPIView, GetFollowedPostsAPIView, CreateCommentAPIView, LikePostsAPIView, FollowUserAPIView, GetSuggestedPostsAPIView, GetSuggestedUsersAPIView, GetUserProfileAPIView, GetUsersAPIView, GetBotAPIView

urlpatterns = [
    path("register/", BotRegistrationAPIView.as_view(), name="register"),
    path("create_post/", CreatePostAPIView.as_view(), name="create_post"),
    path("get_posts/<int:user_id>/", GetPostsAPIView.as_view(), name="get_posts"),
    path("get_followed_posts/<int:user_id>", GetFollowedPostsAPIView.as_view(), name="get_posts"),
    path("comment/", CreateCommentAPIView.as_view(), name="create_comment"),
    path("like/", LikePostsAPIView.as_view(), name="like_posts"),
    path("follow/", FollowUserAPIView.as_view(), name="follow_user"),
    path("suggested_posts/", GetSuggestedPostsAPIView.as_view(), name="suggested_posts"),
    path("suggested_profiles/", GetSuggestedUsersAPIView.as_view(), name="suggested_profiles"),
    path("get_bot/<int:user_id>/", GetBotAPIView.as_view(), name="get_bots"),


        
    ### checking ###
    ### string parameter ###
    path("profile/<str:user>/", GetUserProfileAPIView.as_view(), name="get_profile"),
    path("users", GetUsersAPIView.as_view(), name="get_profile"),

    
]
"""path("bot/get_bots", GetBots.as_view(), name="get_bots"),
    path("bot/create_review", CreatePostAPIView.as_view(), name="create_review"),
    path("bot/delete_review/<int:pk>", BotDeleteReview.as_view(), name="delete_review"),
    path("bot/like_post", LikePost.as_view(), name="like_post"),
    path("bot/get_other_bot_posts/<int:user_id>", GetOtherBotPosts.as_view(), name="get_other_bot_posts"),
    path("bot/get_post_comments/<int:post_id>", GetPostComments.as_view(), name="get_post_comments"),    
    path("bot/get_bot_profile/<int:user_id>", GetBotProfile.as_view(), name="get_bot_profile"),
    path("bot/get_suggested_posts/<int:user_id>", getSuggestedPosts.as_view(), name="get_suggestions"),
    path("bot/get_suggested_users/<int:user_id>", GetSuggestedBots.as_view(), name="get_suggested_bots"),
    path("bot/follow", FollowBot.as_view(), name="follow_bot"),
    path("bot/get_followed_posts/<int:user_id>", GetFollowedPosts.as_view(), name="get_followed_posts"),
    path("bot/delete_comment/<int:pk>", DeleteComment.as_view(), name="delete_comment"),
    path("bot/change_comment", ChangeComment.as_view(), name="change_comment"),
    path("bot/create_comment", CreateComment.as_view(), name="create_comment"),
    path("bot/get_comment/<int:comment_id>", GetComment.as_view(), name="get_comment"),


    path("bot/register/", BotRegistrationAPIView.as_view(), name="register"),"""