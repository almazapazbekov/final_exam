from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import IntegrityError

from news.models import NewsStatus, Status


class LikeDislikeMixIn:
    status_model = None
    object_name = None

    def set_status(self, request, status):
        obj = self.get_object()
        author = request.user.author
        kwargs = {
            self.object_name: obj,
            'author': author,
            'status': get_object_or_404(Status, slug=status)
        }

        try:
            news_status = self.status_model(**kwargs)
            news_status.save()
        except IntegrityError:
            news_status = self.status_model.objects.filter(**kwargs).first()
            if news_status is None:
                data = {
                    "error": "You already added status"
                }
            else:
                news_status.delete()
                data = {
                    "message": 'Like/dislike отозван'
                }

        else:
            data = {
                "message": "Status added"
            }

        return data

    @action(methods=['GET', ], detail=True)
    def like(self, request, pk=None, **kwargs):
        data = self.set_status(request, status='like')
        return Response(data=data, status=200)

    @action(methods=['GET', ], detail=True)
    def dislike(self, request, pk=None, **kwargs):
        data = self.set_status(request, status='dislike')
        return Response(data=data, status=200)


 # def set_status(self, request, status):
    #     obj = self.get_object()
    #     author = request.user.author
    #     kwargs = {
    #         'news': obj,
    #         'author': author,
    #         'status': get_object_or_404(Status, slug=status)
    #     }
    #
    #     try:
    #         news_status = NewsStatus(**kwargs)
    #         news_status.save()
    #     except IntegrityError:
    #         news_status = NewsStatus.objects.filter(**kwargs).first()
    #         if news_status is None:
    #             data = {
    #                 "error": "You already added status"
    #             }
    #         else:
    #             news_status.delete()
    #             data = {
    #                 "message": 'Like/dislike отозван'
    #             }
    #
    #     else:
    #         data = {
    #             "message": "Status added"
    #         }
    #     statuses = NewsStatus.objects.all()
    #     for statusis in statuses:
    #         print(statusis.status.slug)
    #     return data
    #
    # @action(methods=['GET', ], detail=True)
    # def like(self, request, pk=None):
    #     data = self.set_status(request, status='like')
    #
    #     return Response(data=data, status=200)
    #
    # @action(methods=['GET', ], detail=True)
    # def dislike(self, request, pk=None):
    #     data = self.set_status(request, status='dislike')
    #     return Response(data=data, status=200)

