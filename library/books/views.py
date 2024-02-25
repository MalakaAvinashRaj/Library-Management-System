from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Book, Transaction, Reservation
from django.utils import timezone
from django.contrib.auth.models import User

@login_required
def show_books(request):
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})

@login_required
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        Book.objects.create(title=title, author=author, isbn=isbn, status='available')
        messages.success(request, 'Book added successfully.')
        return redirect(reverse('show_books'))
    return render(request, 'add_book.html')

@login_required
def remove_book(request, book_id):
    if request.method == 'POST':  # Ensure that the view only processes POST requests for security reasons
        book = get_object_or_404(Book, pk=book_id)
        book.delete()
        messages.success(request, 'Book removed successfully.')
    else:
        messages.error(request, 'Invalid request.')
    return redirect(reverse('show_books'))

@login_required
def return_book(request, book_id):
    book  = Book.objects.get(id=book_id)
    reservation = get_object_or_404(Reservation, book=book, user=request.user)
    reservation.delete()
    
    transaction = Transaction.objects.get(book=book, user=request.user)
    transaction.return_date = timezone.now()
    transaction.save()
    transaction.book.status = 'available'
    transaction.book.save()
    messages.success(request, f'You have returned {transaction.book.title}.')
    return redirect(reverse('show_books'))

@login_required
def reserve_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if book.status == 'available':
        return_date = timezone.now() + timezone.timedelta(days=14)
        Reservation.objects.create(book=book, user=request.user, reservation_date=timezone.now(), return_date=return_date)
        transaction = Transaction.objects.create(book=book, user=request.user, checkout_date=timezone.now(), return_date=return_date)
        transaction.save()
        book.status = 'not available'
        book.save()
        
        messages.success(request, f'{book.title} has been reserved.')
    else:
        messages.error(request, 'This book is currently not available and cannot be reserved.')
    return redirect(reverse('show_books'))

# @login_required
# def cancel_reservation(request, reservation_id):
#     reservation = get_object_or_404(Reservation, pk=reservation_id, user=request.user)
#     book_id = reservation.book.id
#     reservation.delete()
    
#     book = Book.objects.get(id=book_id)
#     book.status = "available"
#     book.save()
#     messages.success(request, 'Reservation canceled successfully.')
#     return redirect(reverse('show_books'))


def index(request):
    return render(request, 'index.html')

@login_required
def my_transactions(request):
    # Retrieve all transactions for the current logged-in user
    transactions = Transaction.objects.filter(user=request.user).order_by('-checkout_date')
    return render(request, 'my_transactions.html', {'transactions': transactions})

@login_required
def my_reservations(request):
    # Retrieve all reservations for the current logged-in user
    reservations = Reservation.objects.filter(user=request.user).order_by('-reservation_date')
    # transc_id = Transaction.objects.filter(book=reservations.book)
    # print(transc_id)
    return render(request, 'my_reservations.html', {'reservations': reservations})

@login_required
def renew_book(request, book_id):
    # Retrieve the transaction and update the return date
    
    transaction = get_object_or_404(Transaction, book=book_id)
    # You need to decide on the renewal logic here, for example, extend the due date by 14 days
    transaction.return_date = timezone.now() + timezone.timedelta(days=14)
    transaction.save()
    messages.success(request, f'You have successfully renewed {transaction.book.title}.')
    return redirect(reverse('my_reservations'))

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                messages.success(request, 'You are now registered and can log in')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('show_books'))
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))

