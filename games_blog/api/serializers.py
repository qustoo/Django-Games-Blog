from blog.models import Article, Comment
from rest_framework import serializers


class CommentSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    content = serializers.CharField(max_length=500)
    created = serializers.DateTimeField()

    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.content = validated_data.get("content", instance.content)
        return instance


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
