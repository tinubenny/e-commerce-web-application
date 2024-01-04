from django.db import models

# Create your models here.
class EkartAdmin(models.Model):
    user_name = models.CharField(max_length=50)
    passsword = models.CharField(max_length=50)

    class Meta:
        db_table = 'admin_tb'

class Category(models.Model):
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    cover_picture = models.ImageField(upload_to='category/')

    class Meta:
        db_table = 'category_tb'

    def __str__(self):
        return self.category