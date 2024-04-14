from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField


class Address(models.Model):
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=50)
    state = models.CharField(max_length=200)
    land_mark = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.address_line_1}, {self.address_line_2}'

class Customer(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    phone = PhoneNumberField()
    pic = models.ImageField(upload_to='Customer/', null=True)
    address = models.OneToOneField('Address', on_delete=models.CASCADE)
    properties = models.ManyToManyField('Property', related_name='customer')

    def __str__(self) -> str:
        return f'{self.name}'
    
class Property(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    value = models.DecimalField(max_digits=8, decimal_places=2)
    weight_grams = models.IntegerField()
    weight_milligrams = models.IntegerField()
    pic = models.ImageField(upload_to='Property/')

    def __str__(self) -> str:
        return f'{self.name} ({self.value})'

class Loan(models.Model):
    user = models.ForeignKey('Customer', on_delete=models.CASCADE)
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=8, decimal_places=2)
    total_payable = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    loan_repaid = models.DecimalField(max_digits=8, decimal_places=2)
    intrest_rate = models.DecimalField(max_digits=3, decimal_places=2)
    no_of_dues = models.IntegerField()
    when = models.DateTimeField(auto_now_add=True)
    dues = models.ManyToManyField("home.Due", related_name=("Dues_of_Loan"))
    
class Due(models.Model):
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE)
    due_state = (
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
        ('pending', 'pending'),
        ("partially_paid", "partially_paid"),
    )
    due_status = models.CharField(max_length=20, choices=due_state)
    due_amount = models.DecimalField(max_digits=8, decimal_places=2)
    int_due = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    pri_due = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    due_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    paid_date = models.DateField(null=True)
    nth_due = models.PositiveIntegerField()
    payment_mode = (
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
        ('NEFT', 'NEFT'),
        ('UPI', 'UPI'),
    )
    payment_mode = models.CharField(max_length=20, choices=payment_mode, null=True, blank=True)
    
    