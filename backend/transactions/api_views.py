from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import DateFilter, FilterSet
from .models import Status, Type, Category, Subcategory, Transaction
from .serializers import (
    StatusSerializer, TypeSerializer, CategorySerializer,
    SubcategorySerializer, TransactionSerializer
)

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']

class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

# Кастомный фильтр, содержащий фильтрацию по периоду дат
class TransactionFilter(FilterSet):
    date_from = DateFilter(field_name='operation_date', lookup_expr='gte')
    date_to = DateFilter(field_name='operation_date', lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['status', 'type', 'category', 'subcategory']

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().select_related(
        'status', 'type', 'category', 'subcategory'
    )
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TransactionFilter
    # filterset_fields = ['status', 'type', 'category', 'subcategory']
    ordering_fields = ['operation_date', 'amount']
    ordering = ['-operation_date']
