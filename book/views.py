import json
from django.http import JsonResponse
from django.shortcuts import render

from book.models import Book, Category


# Create your views here.

def index(request):
    return render(request, 'base.html')


def book_list(request):
    books = Book.objects.all()
    books_ = []
    for book in books:
        books_.append({
            'title': book.title,
            'author': book.author.full_name,
            'price': book.price,
            'publish_date': book.publish_date,
            'category': book.category,
        })
    return JsonResponse(books_, safe=False)


def book_detail(request, book_id):
    book = Book.objects.filter(id=book_id).first()
    if not book:
        return JsonResponse({'error': 'Book not found'}, status=404)
    return JsonResponse({
        'title': book.title,
        'author': book.author.full_name,
        'price': book.price,
        'publish_date': book.publish_date,
        'category': book.category,
    })


def book_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            book = Book.objects.create(
                title=data['title'],
                author_id=data['author'],
                price=data.get('price', 12),
                publish_date=data.get('publish_date'),
                category=data.get('category', Category.BADIIY),
            )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        return JsonResponse({
            'title': book.title,
            'author': book.author.full_name,
            'price': book.price,
            'publish_date': book.publish_date,
            'category': book.category,
        })


def about(request):
    return render(request, 'about.html')
