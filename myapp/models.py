from django.db import models
from django.contrib.auth.models import User
from django import forms

# List of Tanzanian regions (same as in the model)
TANZANIA_REGIONS = [
    ('Arusha', 'Arusha'),
    ('Dar es Salaam', 'Dar es Salaam'),
    ('Dodoma', 'Dodoma'),
    ('Geita', 'Geita'),
    ('Iringa', 'Iringa'),
    ('Kagera', 'Kagera'),
    ('Katavi', 'Katavi'),
    ('Kigoma', 'Kigoma'),
    ('Kilimanjaro', 'Kilimanjaro'),
    ('Lindi', 'Lindi'),
    ('Manyara', 'Manyara'),
    ('Mara', 'Mara'),
    ('Mbeya', 'Mbeya'),
    ('Morogoro', 'Morogoro'),
    ('Mtwara', 'Mtwara'),
    ('Mwanza', 'Mwanza'),
    ('Njombe', 'Njombe'),
    ('Pemba North', 'Pemba North'),
    ('Pemba South', 'Pemba South'),
    ('Rukwa', 'Rukwa'),
    ('Ruvuma', 'Ruvuma'),
    ('Shinyanga', 'Shinyanga'),
    ('Singida', 'Singida'),
    ('Simiyu', 'Simiyu'),
    ('Songwe', 'Songwe'),
    ('Tabora', 'Tabora'),
    ('Tanga', 'Tanga'),
]

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=255)
    product_types = models.TextField(help_text="List of product categories sold, separated by commas")

    def __str__(self):
        return self.shop_name

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()  # Store price as an integer
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    location = models.CharField(
        max_length=50,  # Maximum length for the location field
        choices=TANZANIA_REGIONS, default=''
    )

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
