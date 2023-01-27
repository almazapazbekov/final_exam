from django.contrib import admin

from .models import Author, user
from news.models import NewsStatus

admin.register(Author)
admin.register(user)
admin.register(NewsStatus)


