from django.contrib import admin
from .models import Address, Customer, Due, Loan, Property
# Register your models here.

class AddressAdmin(admin.ModelAdmin):
    list_display = ['address_line_1', 'city', 'postal_code', 'state', 'land_mark']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'phone', 'address']

class PropertyAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'value', 'weight_grams', 'weight_milligrams']

class LoanAdmin(admin.ModelAdmin): 
    list_display = ['user', 'property', 'loan_amount', 'loan_repaid', 'intrest_rate', 'no_of_dues']

class DueAdmin(admin.ModelAdmin):
    list_display = ['loan', 'due_status', 'due_amount', 'paid_amount', 'due_date', 'paid_date']

admin.site.register(Address, AddressAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.register(Due, DueAdmin)


