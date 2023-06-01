from rest_framework import generics, permissions
from .models import User, Post, Like
from .serializers import UserSerializer, PostSerializer, LikeSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Post, Like,User

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionError("You are not allowed to delete this post.")
        super().perform_destroy(instance)

class LikeCreateView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class LikeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

@login_required
@require_http_methods(["GET", "PUT", "DELETE"])
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "GET":
        if post.is_public or post.owner == request.user:
            likes = Like.objects.filter(post=post)
            response = {
                'post': {
                    'id': post.id,
                    'title': post.title,
                    'content': post.content,
                    'owner': post.owner.username,
                    'is_public': post.is_public,
                },
                'likes': [like.user.username for like in likes]
            }
            return JsonResponse(response)
        else:
            return JsonResponse({'error': 'You do not have permission to access this post.'}, status=403)
    elif request.method == "PUT":
        if post.owner == request.user:
            new_title = request.POST.get('title')
            post.title = new_title
            post.save()

            return JsonResponse({'success': 'Post updated successfully'})
        else:
            return JsonResponse({'error': 'You do not have permission to update this post.'}, status=403)
    elif request.method == "DELETE":
        if post.owner == request.user:
            post.delete()
            return JsonResponse({'success': 'Post deleted successfully'})
        else:
            return JsonResponse({'error': 'You do not have permission to delete this post.'}, status=403)

