from django.contrib import admin

from .models import Status, Type, Category, Subcategory, Transaction
from .forms import TransactionForm

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    list_filter = ['type']
    search_fields = ['name']

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category', 'category__type']
    search_fields = ['name']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    form = TransactionForm
    list_display = ['operation_date', 'type', 'category', 'subcategory', 'amount', 'status']
    list_filter = ['status', 'type', 'category', 'operation_date']
    search_fields = ['comment', 'category__name']
    date_hierarchy = 'operation_date'
