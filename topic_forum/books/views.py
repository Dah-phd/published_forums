from django.shortcuts import render
from django.contrib import messages
from .models import book
from .forms import contact_form


def main(request):
    return render(request, 'books/books.html', {'books': book.objects.all().order_by('-published')})


def contact_page(request):
    if request.method == 'POST':
        form = contact_form(request.POST)
        if form.is_valid():
            messages.success(request, 'message send')
            obj = form.save(commit=False)
            if request.user.is_authenticated:
                obj.contact = request.user
                obj.email = request.user.email
            else:
                obj.email = request.POST['mail']
            obj.save()
    return render(request, 'books/contact.html', {'books': book.objects.all(), 'form': contact_form})


def support(request):
    return render(request, 'books/support.html', {'books': book.objects.all()})
