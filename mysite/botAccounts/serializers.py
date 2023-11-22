from accounts.models import CustomUser
from accounts.serializers import PostSerializer
from rest_framework import serializers

class BotSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    is_bot = serializers.BooleanField(default=True)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', "posts", "is_bot", 'followers_count', 'created_at',)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user