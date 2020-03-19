from django.urls import path

from .views import CartView, CartDeleteView, DeliveryView, placeorder


urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/delete', CartDeleteView.as_view(), name='deletecart'),
    path('cart/place', placeorder, name='placeorder'),

    path('deliveries/', DeliveryView.as_view(), name='deliveries'),
    path('deliveries/done', DeliveryView.as_view(), name='deliveries'),
]
