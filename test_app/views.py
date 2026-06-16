from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)

from .models import Post
from .serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly
from.models import Comment


class PostListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Post.objects.filter(
            is_published=True
        ).select_related("author")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Post.objects.select_related(
        "author"
    ) 

class CommentListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.kwargs["post_id"]
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post_id=self.kwargs["post_id"]
        )           
