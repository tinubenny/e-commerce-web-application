from django.db import models

from eKart_admin.models import Category

# Create your models here.
class Seller(models.Model):
    first_name = models.CharField(max_length=25)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    company_name = models.CharField(max_length=25)
    email = models.CharField(max_length=25)
    gender = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    country = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    profile_image = models.ImageField(upload_to="seller/")
    login_id = models.IntegerField(null=True)
    account_number = models.BigIntegerField(default=0)
    bank_name = models.CharField(max_length=20)
    bank_branch = models.CharField(max_length=20, default ='')
    ifsc_code = models.CharField(max_length=20)
    status = models.CharField(max_length=50,default='pending') 
    
    class Meta:
        db_table = 'seller_tb'

class Product(models.Model):
    product_no = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete = models.CASCADE)
    product_name = models.CharField(max_length=30)
    description = models.CharField(max_length= 200)
    stock = models.IntegerField()
    price = models.FloatField()
    image = models.ImageField(upload_to="Product/")
    rating = models.FloatField(default = 0)
    status = models.CharField(max_length=30, default ='available')

    class Meta:
        db_table = 'product_tb'

    
    
    
    
