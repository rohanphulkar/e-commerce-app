from django.db import models
import uuid
from accounts.models import User
from autoslug import AutoSlugField
# Create your models here.
class Product(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name = models.CharField(max_length=100,default="")
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='products/')
    slug = AutoSlugField(populate_from='name',unique_with=['id'])
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True, blank=True)
    email = models.CharField(max_length=100,null=True, blank=True)
    phone = models.CharField(max_length=100,null=True, blank=True)
    address = models.CharField(max_length=100,null=True, blank=True)
    state = models.CharField(max_length=100,null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    pincode = models.CharField(max_length=7,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=100,null=True, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name