from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import State, City, KartUser, Order, OrderItem


class KartUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'city', 'dob', 'account_type')}
         ),
    )
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password', 'city', 'dob', 'account_type', 'currency')}),
    )
    model = KartUser
    list_display = ['email', 'username', ]


admin.site.register(State)
admin.site.register(City)
admin.site.register(KartUser, KartUserAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
