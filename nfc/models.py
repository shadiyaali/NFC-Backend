from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import AdminManager
from django.contrib.auth.hashers import make_password
from datetime import timedelta, date


class Admin(AbstractUser):
    username = None  
    email = models.EmailField(unique=True)  
    is_admin = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="admin_users",  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="admin_users_permissions",  
        blank=True
    )

    objects = AdminManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"




class Vendor(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Block', 'Block'),              
    ]
    username = models.CharField(max_length=255, unique=True, null=True, blank=True) 
    vendor_name = models.CharField(max_length=255, null=True, blank=True) 
    address = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True) 
    city = models.CharField(max_length=255, null=True, blank=True) 
    contact_person = models.CharField(max_length=255, null=True, blank=True) 
    contact_number1 = models.CharField(max_length=50, null=True, blank=True)
    contact_number2 = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    website = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to='vendor_logos/', null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)  
    sub_domain = models.TextField(max_length=50, null=True, blank=True)
    status =  models.CharField(max_length=255, choices=STATUS_CHOICES , default='Active',blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)   
        super().save(*args, **kwargs)

    def __str__(self):
        return self.vendor_name or str(self.username)
    


class Templates(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to='templates/', null=True, blank=True)  

    def __str__(self):
        return self.name or "Unnamed Template"


class Subscription(models.Model):
    plan_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    validity = models.IntegerField(help_text="Validity in days", null=True, blank=True)

    def __str__(self):
        return self.plan_name or "Unnamed Plan"


class Users(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Block', 'Block'),
    ]
    APPROVAL_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]    
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=50, null=True, blank=True)
    mobile_number = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    website = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to='user_logos/', null=True, blank=True)
    facebook = models.TextField(null=True, blank=True)
    instagram = models.TextField(null=True, blank=True)
    youtube = models.TextField(null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True) 
    location_map = models.TextField(null=True, blank=True) 
    template = models.ForeignKey(Templates, on_delete=models.SET_NULL, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Active', blank=True, null=True)
    approval_status = models.CharField(max_length=255, choices=APPROVAL_CHOICES, default='Pending', blank=True, null=True)
  
    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)  
       
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name or str(self.username)



    

class Subscribers(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    plan = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.plan and self.plan.validity:
            self.expiry_date = date.today() + timedelta(days=self.plan.validity)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.name if self.user else "Unnamed User"




class Receivables(models.Model):
    Mode_CHOICES = [
        ('Bank', 'Bank'),
        ('Cash', 'Cash'),
        ('G Pay', 'G Pay'),
    ]
    vendor_name = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    plan = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    received = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, editable=True)
    pay = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    mode = models.CharField(max_length=255, choices=Mode_CHOICES, default='Bank', blank=True, null=True)

    def save(self, *args, **kwargs):
        total_received = (self.received or 0) + (self.pay or 0)  
        self.balance = (self.amount or 0) - total_received  

        super().save(*args, **kwargs)

    def __str__(self):
       return self.user.name if self.user and self.user.name else "Unnamed User"

   
    
class Expenses(models.Model):
    expense_type = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
 
        self.balance = (self.amount or 0) - (self.paid or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Expense: {self.expense_type} - Balance: {self.balance}"

