from django.urls import path

from .views import (ProductsListView,
                    ProductDetailView,

                    CartAdd)

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('<str:name>/', ProductDetailView.as_view(), name='product-detail'),
    path('<str:name>/cartadd', CartAdd, name='add_to_cart'),
]
