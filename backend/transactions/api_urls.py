from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    StatusViewSet, TypeViewSet, CategoryViewSet,
    SubcategoryViewSet, TransactionViewSet
)

router = DefaultRouter()
router.register(r'statuses', StatusViewSet)
router.register(r'types', TypeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
