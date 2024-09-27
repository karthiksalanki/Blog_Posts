from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','first_name', 'last_name',]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    # author = UserSerializer() 
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'creation_date', 'tags']

    # def create(self, validated_data):
    #     tags_data = validated_data.pop('tags', [])
    #     print(tags_data)
    #     post = BlogPost.objects.create(**validated_data)
    #     for tag_data in tags_data:
    #         try:
    #             tag, created = Tag.objects.get_or_create(name=tag_data['name'])
    #             print(tag)
    #             post.tags.add(tag)
    #         except IntegrityError:
    #             tag = Tag.objects.get(name=tag_data['name'])
    #     return post

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at']