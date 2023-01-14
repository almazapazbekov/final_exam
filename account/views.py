from django.shortcuts import render
from rest_framework import generics, viewsets, mixins, status
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import AuthorSerializer \
    # ,TokenSerializer
from .models import Author


class AuthorRegisterView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


# class TokenAPI(generics.CreateAPIView):
#     queryset = obtain_auth_token
#     serializer_class = TokenSerializer
