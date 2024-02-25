from django.contrib import admin
from .models import Book, UserProfile, Transaction, Reservation

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'status')  # Columns to display in the admin list view
    search_fields = ('title', 'author')  # Fields to search in the admin list view
    list_filter = ('status',)  # Filters to apply in the admin list view

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'checkout_date', 'return_date')
    list_filter = ('checkout_date', 'return_date')
    search_fields = ('book__title', 'user__username')



admin.site.register(Book, BookAdmin)
admin.site.register(Transaction, TransactionAdmin)

admin.site.register(UserProfile)  # No customizations for UserProfile
admin.site.register(Reservation)  # No customizations for Reservation