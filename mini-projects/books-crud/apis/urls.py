from django.urls import path

from apis.views import BookListAPI

urlpatterns = [
    path("",BookListAPI.as_view())
]