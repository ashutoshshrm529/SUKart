from django.shortcuts import render, redirect
from django.views.generic import (ListView,
                                  DetailView)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count

from .models import Product
from Users.models import KartUser, Order, OrderItem


class ProductsListView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    slug_field = 'name'
    slug_url_kwarg = 'name'
    template_name = 'product.html'
    context_object_name = 'product'


@login_required
def CartAdd(request, *args, **kwargs):
    if request.user.is_authenticated:
        if request.user.account_type == 'Customer' and request.user.is_superuser != True:
            if not request.user.orders.filter(status='Not Placed').first():
                Distributor = KartUser.objects.filter(
                    account_type='Distributor').filter(city=request.user.city)
                if Distributor.count() == 0:
                    Distributor = KartUser.objects.filter(
                        account_type='Distributor').filter(city__in=request.user.city.state.cities.all())
                    if Distributor.count() == 0:
                        Distributor = KartUser.objects.filter(account_type='Distributor')

                Distributor = Distributor.annotate(count=Count(
                    'deliveries')).order_by('count').first()

                order = Order.objects.create(distributor=Distributor,
                                             customer=request.user,
                                             status='Not Placed')
                order.save()

            item, created = OrderItem.objects.get_or_create(product=Product.objects.filter(name=kwargs['name']).first(),
                                                            order=request.user.orders.filter(status='Not Placed').first())
            if created:
                item.save()
                messages.success(request, 'Item successfully added')

            return redirect('cart', request.user.username)
        else:
            messages.error(request, 'You are not a customer and do not have a cart')
            return redirect('index')
