from django.urls import path

from books.views import BookList

urlpatterns =[
    path("all",BookList.as_view())
]