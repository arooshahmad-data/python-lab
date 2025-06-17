from django.shortcuts import render
from rest_framework import generics

from apis.serializers import BookSerializer
from books.models import Book


# Create your views here.

class BookListAPI(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
