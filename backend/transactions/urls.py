from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('', views.TransactionListView.as_view(), name='transaction_list'),
    path('create/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='transaction_edit'),
    path('<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction_delete'),
]
