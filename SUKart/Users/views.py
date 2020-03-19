from django.shortcuts import render
from django.views.generic import (ListView,
                                  DetailView,
                                  DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import KartUser, Order, OrderItem
from .forms import CustomerRegisterForm, DistributorRegisterForm, UserUpdateForm


class CartView(ListView):
    model = OrderItem
    template_name = 'orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return KartUser.objects.get(username=self.kwargs['name']).orders.filter(status='Not Placed').first().products.all


class CartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    slug_field = 'customer__username'
    slug_url_kwarg = 'name'
    template_name = 'order_confirm_delete.html'
    context_object_name = 'order'
    success_url = '/'

    def test_func(self):
        order = self.get_object()
        if self.request.user == order.customer:
            return True
        return False


def placeorder(request, *args, **kwargs):
    if request.user.username == kwargs['username']:
        price = 0
        for cartitem in request.user.carts.filter(status='Not Placed').first().products.all():
            price += cartitem.product.selling_price
        if request.user.currency >= price:
            request.user.currency -= price
            request.user.save()
            cart = Cart.objects.filter(customer=request.user).filter(status='Not Placed').first()
            cart.status = 'Placed'
            cart.save()

            send_mail('Order Placed',
                      'Order will be delivered by -'+cart.distributor.username +
                      '\n Order id -'+str(cart.id),
                      settings.EMAIL_HOST_USER,
                      {request.user.email, })

            messages.success(request, 'Order Placed')
            return redirect('index')
        else:
            messages.success(request, 'Low Balance')
            return redirect('index')
    else:
        messages.success(request, 'You can only place your own orders')
        return redirect('index')


class DeliveryView(ListView):
    model = OrderItem
    template_name = 'deliveries.html'
    context_object_name = 'deliveries'

    def get_queryset(self):
        return KartUser.objects.get(username=self.kwargs['name']).deliveries.products


def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            form.account_type = 'Customer'
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to login')
            return redirect('login')
    else:
        form = CustomerRegisterForm()
    return render(request, 'register.html', {'form': form})


def register_distributor(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            form.account_type = 'Distributor'
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to login')
            return redirect('login')
    else:
        form = CustomerRegisterForm()
    return render(request, 'register.html', {'form': form})
