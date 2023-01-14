from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework.views import APIView

from news.models import News, Comment, Status, CommentStatus, NewsStatus
from news.serializers import NewsSerializer, CommentSerializer, StatusSerializer
from .permissions import IsAuthenticated, IsOwnerPermission
from .mixins import LikeDislikeMixIn


class NewsViewSet(LikeDislikeMixIn, viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated, ]

    status_model = NewsStatus
    object_name = 'news'

    filter_backends = [DjangoFilterBackend]
    search_fields = ['title', ]
    ordering_fields = ['created', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)


class CommentListCreateAPIView(LikeDislikeMixIn, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    status_model = CommentStatus
    object_name = 'comment'

    # def get_queryset(self):
    #     return super().get_queryset().filter(news_id=self.kwargs.get('news_id'))
    #
    # def perform_create(self, serializer):
    #     serializer.save(
    #         news_id=self.kwargs.get('news_id'),
    #         author=self.request.user.author
    #     )


class StatusListCreateAPIView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAdminUser, ]


class StatusRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAdminUser, ]

# class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsOwnerPermission, ]
#
#     def get_queryset(self):
#         return super().get_queryset().filter(comment_id=self.kwargs.get('comment_id'))

#
# class LikeDislikeCommentApiView(APIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsOwnerPermission, ]
#
#     def get_queryset(self):
#         return super().get_queryset().filter(news_id=self.kwargs.get('news_id'))
#
#     def set_status(self, request, status):
#         obj = self.get_object()
#         author = request.user.author
#         kwargs = {
#             'news': obj,
#             'author': author,
#             'status': get_object_or_404(Status, slug=status)
#         }
#
#         try:
#             news_status = CommentStatus(**kwargs)
#             news_status.save()
#         except IntegrityError:
#             news_status = CommentStatus.objects.filter(**kwargs).first()
#             if news_status is None:
#                 data = {
#                     "error": "You already added status"
#                 }
#             else:
#                 news_status.delete()
#                 data = {
#                     "message": 'Like/dislike отозван'
#                 }
#
#         else:
#             data = {
#                 "message": "Status added"
#             }
#         statuses = CommentStatus.objects.all()
#         for statusis in statuses:
#             print(statusis.status.slug)
#         return data
#
#     @action(methods=['GET', ], detail=True)
#     def like(self, request, pk=None):
#         data = self.set_status(request, status='like')
#
#         return Response(data=data, status=200)
#
#     @action(methods=['GET', ], detail=True)
#     def dislike(self, request, pk=None):
#         data = self.set_status(request, status='dislike')
#         return Response(data=data, status=200)
