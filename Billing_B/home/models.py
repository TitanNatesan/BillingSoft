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
    pic = models.ImageField(upload_to='Customer/', null=True)
    property = models.ForeignKey("home.Property", on_delete=models.CASCADE, null=True)
    address = models.OneToOneField("home.Address", on_delete=models.CASCADE,null=True)
    phone = PhoneNumberField()

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


class Reciept(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) #<------------------------------------
    property = models.OneToOneField(Property, on_delete=models.CASCADE) #<---------------------------------
    
    when = models.DateTimeField(auto_now_add=True)  # receipt issued date and time
    loan_amount = models.DecimalField(max_digits=8, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5,decimal_places=2,validators=[MinValueValidator(0.01, message="Value must be greater than or equal to 0.01"),MaxValueValidator(100, message="Value must be less than or equal to 100"),])
    total_dues = models.IntegerField()  # total no. of dues to pay
    m_opt = (
    ('January', 'January'),
    ('February', 'February'),
    ('March', 'March'),
    ('April', 'April'),
    ('May', 'May'),
    ('June', 'June'),
    ('July', 'July'),
    ('August', 'August'),
    ('September', 'September'),
    ('October', 'October'),
    ('November', 'November'),
    ('December', 'December'),
)
    due_done = ArrayField(models.CharField(max_length=50,choices=m_opt,null=True,blank=True),null=True,blank=True)  # no. of dues paid
    due_skip = ArrayField(models.CharField(max_length=50,choices=m_opt,null=True,blank=True),null=True,blank=True)
    
    r_opt = (
        ('Pending',"Pending"), 
        ("Finished","Finished"),
    )
    status = models.CharField(max_length=50,choices=r_opt)
    
class Loan(models.Model):
    amount_paid = models.DecimalField( max_digits=8, decimal_places=2,null=True)
    is_paid = models.BooleanField(null=True,blank=True)
    receipt = models.ForeignKey(Reciept,on_delete=models.CASCADE)
    due_date = models.DateTimeField(null=True,blank=True)
    
    def __str__(self) -> str:
        return f'{self.due_date}'

class Due(models.Model):
    
    pass