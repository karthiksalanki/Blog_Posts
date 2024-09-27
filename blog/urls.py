from django.urls import path
from .views import *

urlpatterns = [
    # User Authentication
    path('register/', register, name='register_user'),
    path('login/', login, name='login'),

    # CRUD operations on posts 
    path('posts/', posts, name='posts'),     # list of posts for advanced features(with pagination) and create posts
    path('post/<int:pk>/', post_detail, name='post_detail'),    # alter posts

    # Comments and Tags:
    path('comment/', comment, name='comment'),  # add comment
    path('max_comments/',max_comments, name="max_comments"),    # top 5 commented posts
    path('posts/tag/<str:tag_name>/',posts_by_tag, name="posts_by_tag"),   # post by tag name
    path('tags/', tags, name="tag"),    # add tags

    # Advanced Features
    path('search/posts/', search_post, name="search_post")  # search post based on keywords

]