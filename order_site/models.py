from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    username = models.CharField(blank=False, max_length=100, unique=True)
    password = models.CharField(blank=False, max_length=100)
    first_name = models.CharField(blank=False, max_length=100)
    last_name = models.CharField(blank=False, max_length=100)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(blank=False, null=True, max_length=254)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=200)
    imageUrl = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(blank=False, max_length=200)
    price = models.IntegerField(blank=False)
    description = models.CharField(blank=False, max_length=500)
    imageUrl = models.CharField(blank=False, max_length=500)
    is_gluten_free = models.BooleanField(default=False)
    is_vegeterian = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Delivery(models.Model):
    is_delivered = models.BooleanField(default=False)
    address = models.CharField(blank=False, max_length=200)
    notes = models.CharField(max_length=500)
    created = models.DateTimeField(null=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery = models.OneToOneField(
        Delivery, on_delete=models.CASCADE, primary_key=True)


class Items(models.Model):
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
