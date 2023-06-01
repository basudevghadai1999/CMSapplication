
from django.urls import path
from . import views

urlpatterns = [
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
]
