from django.contrib import admin
from .models import Customer,Property,Reciept,Address
# Register your models here.

class AdminCustomer(admin.ModelAdmin):
    list_display=[
        'name',
        'address',
        'property',
    ]
admin.site.register(Customer,AdminCustomer)

class AdminProperty(admin.ModelAdmin):
    list_display=[
        'name',
        'value',
        'weight_grams',
    ]
admin.site.register(Property,AdminProperty)

class AdminReciept(admin.ModelAdmin):
    list_display=[
        'customer',
        'property',
        'loan_amount',
        'interest_rate',
        'due_done',
        'due_skip',
        'total_dues',
    ]
admin.site.register(Reciept,AdminReciept)

class AdminAddress(admin.ModelAdmin):
    list_display=[
        'address_line_1',
        'city',
        'postal_code',
        'land_mark',
    ]
admin.site.register(Address,AdminAddress)