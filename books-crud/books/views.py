from django.shortcuts import render
from django.views.generic import ListView
from books.models import Book
# Create your views here.
class BookList(ListView):
    model = Book
    template_name = 'book_list.html'
