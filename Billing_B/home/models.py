from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField


class Customer(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    phone = PhoneNumberField()
    pic = models.ImageField(upload_to='Customer/')
    property = models.ForeignKey("home.Property", on_delete=models.CASCADE, null = True)

class Property(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    value = models.DecimalField(max_digits=8, decimal_places=2)
    weight_grams = models.IntegerField()
    weight_milligrams = models.IntegerField()
    pic = models.ImageField(upload_to='Property/')

class Reciept(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    when = models.TimeField(auto_now_add=True) # reciept issued date and time
    loan_amount = models.DecimalField(max_digits=8, decimal_places=2)
    intrest_rate = models.DecimalField(
        max_digits=5,  # Adjust the value based on your needs
        decimal_places=2,  # Two decimal places
        validators=[
            MinValueValidator(0.01, message="Value must be greater than or equal to 0.01"),
            MaxValueValidator(100, message="Value must be less than or equal to 100"),
        ]
    )
    total_dues = models.IntegerField() #total no. of dues to pay
    due_done = models.IntegerField() #no. of dues payed 
    due_skip = ArrayField(models.PositiveIntegerField()) #which dues are skiped from the initial month of the recipt issued
    pdf = models.FileField(upload_to='Receipt/')
    