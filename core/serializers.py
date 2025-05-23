from rest_framework import serializers
from .models import WordPair

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    is_public = serializers.BooleanField()


    class Meta:
        model = WordPair
        fields = '__all__'

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return user in obj.likes.all()

    def get_is_saved(self, obj):
        user = self.context['request'].user
        return user in obj.saved_by.all()
