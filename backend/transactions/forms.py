from django.shortcuts import render
from django import forms
from django.core.exceptions import ValidationError
from .models import Transaction, Category, Subcategory

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['operation_date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'operation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        type_obj = cleaned_data.get('type')
        amount = cleaned_data.get('amount')

        # Валидация: категория должна относиться к выбранному типу
        if category and type_obj and category.type != type_obj:
            raise ValidationError({
                'category': 'Выбранная категория не относится к выбранному типу операции.'
            })

        # Валидация: подкатегория должна относиться к выбранной категории
        if subcategory and category and subcategory.category != category:
            raise ValidationError({
                'subcategory': 'Выбранная подкатегория не относится к выбранной категории.'
            })

        # Валидация: сумма должна быть положительной
        if amount and amount <= 0:
            raise ValidationError({
                'amount': 'Сумма должна быть положительным числом.'
            })

        return cleaned_data

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None:
            raise ValidationError('Поле "Сумма" обязательно для заполнения.')
        return amount
