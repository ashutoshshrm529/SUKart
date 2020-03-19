from django.db import models
from django.contrib.auth.models import AbstractUser

from Store.models import Product


class State(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=40)
    state = models.ForeignKey(State, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class KartUser(AbstractUser):
    dob = models.DateField()
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    account_type = models.CharField(max_length=11,
                                    choices=[('Distributor', 'Distributor'),
                                             ('Customer', 'Customer'), ],
                                    default='Customer')
    # set to 100 for now. will change to zero later
    currency = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.username


class Order(models.Model):
    customer = models.ForeignKey(KartUser,
                                 related_name='orders',
                                 on_delete=models.CASCADE,
                                 limit_choices_to={'account_type': 'Customer'})
    distributor = models.ForeignKey(KartUser,
                                    related_name='deliveries',
                                    on_delete=models.CASCADE,
                                    limit_choices_to={'account_type': 'Distributor'})
    status = models.CharField(max_length=11,
                              choices=[('Not Placed', 'Not Placed'),
                                       ('Placed', 'Placed'),
                                       ('Delivered', 'Delivered')],
                              default='Not Placed')

    def __str__(self):
        return self.id


class OrderItem(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    order = models.ForeignKey(Order,
                              related_name='products',
                              on_delete=models.CASCADE,)

    def __str__(self):
        return self.product.name
