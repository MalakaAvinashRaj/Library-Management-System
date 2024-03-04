from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=80, null=False)
    author = models.CharField(max_length=80, null=False)
    isbn = models.CharField(max_length=13, unique=True, null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, null=False, default='available')

    def _str_(self):
        return self.title

# Extend the User model using a One-To-One Link
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    transactions = models.ManyToManyField('Transaction', related_name='transactions', blank=True)

    def _str_(self):
        return self.user.username

class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_transactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_transactions')
    checkout_date = models.DateTimeField(null=True)
    return_date = models.DateTimeField(null=True)

    def _str_(self):
        return f"Transaction {self.id}"

class Reservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reservations')
    reservation_date = models.DateTimeField(null=False, default=timezone.now)
    return_date = models.DateTimeField(null=True)
    
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, related_name='reservation', blank=True)

    def __str__(self):
        return f"Reservation {self.id}"