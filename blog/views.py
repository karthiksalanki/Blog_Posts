from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .serializers import *
from .models import *

# Create your views here.
# @permission_classes([AllowAny])
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.set_password(request.data['password'])
                user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'GET':
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        if username != None and  password != None:
            user = authenticate(username=username, password=password)
            if user is None:
                return Response({'message':'invalid password'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
        else:
            return Response({'error':'username an password should not be empty'})
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def posts(request):
    if request.method == 'GET':
        try:
            posts = BlogPost.objects.all()
            paginator = PageNumberPagination()
            paginated_posts = paginator.paginate_queryset(posts, request)
            serializer = BlogPostSerializer(paginated_posts, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'POST':
        try:
            user = User.objects.get(id=request.data['author_id'])
            if request.user.id==user.id:
                tags_data = request.data.pop('tags', [])
                tag_instances = []
                for tag_data in tags_data:
                    tag, created = Tag.objects.get_or_create(name=tag_data['name'])
                    tag_instances.append(tag)
                serializer = BlogPostSerializer(data=request.data)
                if serializer.is_valid():
                    post = serializer.save(author=request.user)
                    post.tags.set(tag_instances)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message':'Not allowed to create this post'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_detail(request, pk):
    try:
        post = BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return Response({'message':'Blogpost not found'},status=status.HTTP_404_NOT_FOUND)

    try:
        if request.method == 'GET':
            serializer = BlogPostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            if post.author != request.user:
                return Response({'message': 'Not allowed to update this post'}, status=status.HTTP_403_FORBIDDEN)

            tags_data = request.data.pop('tags', [])
            tag_instances = []
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(name=tag_data['name'])
                tag_instances.append(tag)
            serializer = BlogPostSerializer(post, data=request.data)
            if serializer.is_valid():
                post = serializer.save(author=request.user)
                post.tags.set(tag_instances)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            if post.author != request.user:
                return Response({'message': 'Not allowed to delete this post'}, status=status.HTTP_403_FORBIDDEN)
            
            post.delete()
            return Response({'message':'deleted'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment(request):
    try:
        post_id = request.data.get('post_id')
        post = BlogPost.objects.get(pk=post_id)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        if request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, post=post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def max_comments(request):
    try:
        maximum_comments = Comment.objects.filter()
        most_commented = BlogPost.objects.annotate(comment_count=models.Count('comments')).order_by('-comment_count')[:5]
        serializer = BlogPostSerializer(most_commented, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def posts_by_tag(request, tag_name):
    try:
        tag = Tag.objects.get(name=tag_name)
    except Tag.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    posts = tag.blog_posts.all()
    serializer = BlogPostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def tags(request):
    try:
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def search_post(request):
    if request.method == 'GET':
        try:
            search_query = request.GET.get('search', None)
            posts = BlogPost.objects.all()

            # If search query is provided, filter the queryset
            if search_query:
                posts = posts.filter(
                    Q(title__icontains=search_query) |  
                    Q(content__icontains=search_query) |  
                    Q(tags__name__icontains=search_query)
                ).distinct()

            paginator = PageNumberPagination()
            paginated_posts = paginator.paginate_queryset(posts, request)

            # Serialize the paginated results
            serializer = BlogPostSerializer(paginated_posts, many=True)

            # Return paginated response
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
