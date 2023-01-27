"""exam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter

from account.views import AuthorRegisterView
from news.views import NewsViewSet, CommentListCreateAPIView, \
    StatusListCreateAPIView, StatusRetrieveUpdateDestroyAPIView \
    # ,LikeDislikeCommentApiView, CommentRetrieveUpdateDestroyAPIView

schema_view = get_schema_view(
    openapi.Info(
        title="НОВОСТНОЙ САЙТ",
        default_version='v0.1',
        description="API Для новостного сайта",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="a2@gmail.com"),
        license=openapi.License(name="Лицензии нет"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

news_router = DefaultRouter()
news_router.register('news', NewsViewSet)

comment_router = DefaultRouter()
comment_router.register('comments', CommentListCreateAPIView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('rest_framework.urls')),
    path('api/account/token/', obtain_auth_token),

    path('api/account/register/', AuthorRegisterView.as_view()),

    path('api/', include(news_router.urls)),
    path('api/news/<int:news_id>/', include(comment_router.urls)),
    # path('api/news/<int:news_id>/comments/', CommentListCreateAPIView.as_view()),
    # path('api/news/<int:news_id>/comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view()),

    path('api/statuses/', StatusListCreateAPIView.as_view()),
    path('api/statuses/<int:pk>/', StatusRetrieveUpdateDestroyAPIView.as_view()),

    # path('api/news/<int:news_id>/comments/<int:pk>/like/', LikeDislikeCommentApiView.as_view()),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc_ui'),
    path('json_doc/', schema_view.without_ui(cache_timeout=0), name='json_doc'),

]
