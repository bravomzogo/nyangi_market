from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


# List of Tanzanian regions
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
    phone = models.CharField(max_length=15, default="N/A")  # NEW FIELD with default

    def __str__(self):
        return self.shop_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True)
    area_of_residence = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    image1 = models.ImageField(upload_to='products/', null=True, blank=True, default="")  # NEW IMAGE
    image2 = models.ImageField(upload_to='products/', null=True, blank=True, default="")
    image3 = models.ImageField(upload_to='products/', null=True, blank=True, default="")
    image4 = models.ImageField(upload_to='products/', null=True, blank=True, default="")
    phone_number=models.CharField(max_length=10 ,default='')
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE)
    location = models.CharField(max_length=50, choices=TANZANIA_REGIONS, default='Dar es Salaam')  # Default region

    # General technical details
    condition = models.CharField(max_length=100, default="New", blank=True)
    dimensions = models.CharField(max_length=100, default="", blank=True)
    weight = models.CharField(max_length=50, default="", blank=True)
    material = models.CharField(max_length=100, default="", blank=True)
    color = models.CharField(max_length=50, default="", blank=True)
    warranty = models.CharField(max_length=50, default="No Warranty", blank=True)
    model = models.CharField(max_length=100, default="", blank=True)
    release_year = models.IntegerField(default="", blank=True, null=True)
    generation = models.CharField(max_length=50, default="", blank=True)
    brand = models.CharField(max_length=100, default="", blank=True)
    origin_country = models.CharField(max_length=100, default="", blank=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    # Electronics & Appliances
    power_consumption = models.CharField(max_length=50, default="", blank=True)
    battery_life = models.CharField(max_length=50, default="", blank=True)
    charging_time = models.CharField(max_length=50, default="", blank=True)
    connectivity = models.CharField(max_length=100, default="", blank=True)
    processor = models.CharField(max_length=100, default="", blank=True)
    storage_capacity = models.CharField(max_length=100, default="", blank=True)
    screen_size = models.CharField(max_length=50, default="", blank=True)
    resolution = models.CharField(max_length=100, default="", blank=True)

    # Furniture & Home Decor
    weight_capacity = models.CharField(max_length=50, default="", blank=True)
    assembly_required = models.BooleanField(default="", blank=True, null=True)
    style = models.CharField(max_length=100, default="", blank=True)
    water_resistant = models.BooleanField(default="", blank=True, null=True)
    upholstery_material = models.CharField(max_length=100, default="", blank=True)

    # Clothing, Shoes & Fashion
    size = models.CharField(max_length=50, default="", blank=True)
    gender = models.CharField(max_length=50, default="", blank=True)
    fabric_type = models.CharField(max_length=100, default="", blank=True)
    washing_instructions = models.TextField(default="", blank=True)
    shoe_type = models.CharField(max_length=100, default="", blank=True)
    closure_type = models.CharField(max_length=100, default="", blank=True)

    # Automobile & Vehicle Accessories
    fuel_type = models.CharField(max_length=50, default="", blank=True)
    transmission = models.CharField(max_length=50, default="", blank=True)
    mileage = models.CharField(max_length=50, default="", blank=True)
    engine_capacity = models.CharField(max_length=50, default="", blank=True)
    top_speed = models.CharField(max_length=50, default="", blank=True)
    number_of_seats = models.IntegerField(default="", blank=True, null=True)

    # Food & Beverages
    expiration_date = models.DateField(null=True, blank=True)
    ingredients = models.TextField(default="", blank=True)
    calories = models.CharField(max_length=50, default="", blank=True)
    dietary_info = models.CharField(max_length=100, default="", blank=True)
    package_size = models.CharField(max_length=100, default="", blank=True)

    # Books, Stationery & Office Supplies
    author = models.CharField(max_length=100, default="", blank=True)
    publisher = models.CharField(max_length=100, default="", blank=True)
    edition = models.CharField(max_length=50, default="", blank=True)
    pages = models.IntegerField(default="", blank=True, null=True)
    language = models.CharField(max_length=50, default="", blank=True)
    paper_type = models.CharField(max_length=100, default="", blank=True)

    # Toys & Games
    recommended_age = models.CharField(max_length=50, default="", blank=True)
    number_of_pieces = models.IntegerField(default="", blank=True, null=True)
    safety_certifications = models.CharField(max_length=100, default="", blank=True)
    battery_required = models.BooleanField(default="", blank=True, null=True)
    interactive_features = models.CharField(max_length=100, default="", blank=True)

    # Health & Beauty
    skin_type = models.CharField(max_length=100, default="", blank=True)
    scent = models.CharField(max_length=100, default="", blank=True)
    application_method = models.CharField(max_length=100, default="", blank=True)
    volume = models.CharField(max_length=50, default="", blank=True)

    # Sports & Outdoor
    sport_type = models.CharField(max_length=100, default="", blank=True)
    weather_resistant = models.BooleanField(default="", blank=True, null=True)
    material_durability = models.CharField(max_length=100, default="", blank=True)

    # Jewelry & Accessories
    gemstone = models.CharField(max_length=100, default="", blank=True)
    metal_type = models.CharField(max_length=100, default="", blank=True)
    weight = models.CharField(max_length=50, default="", blank=True)
    certification = models.CharField(max_length=100, default="", blank=True)

    def __str__(self):
        return self.name

    def get_technical_details(self):
        details = {
            self.condition: "Condition",
            self.dimensions: "Dimensions",
            self.weight: "Weight",
            self.material: "Material",
            self.color: "Color",
            self.warranty: "Warranty",
            self.model: "Model",
            self.release_year: "Year of Release",
            self.generation: "Generation",
            self.brand: "Brand",
            self.origin_country: "Origin Country",
            self.power_consumption: "Power Consumption",
            self.battery_life: "Battery Life",
            self.charging_time: "Charging Time",
            self.connectivity: "Connectivity",
            self.processor: "Processor",
            self.storage_capacity: "Storage Capacity",
            self.screen_size: "Screen Size",
            self.resolution: "Resolution",
            self.weight_capacity: "Weight Capacity",
            self.assembly_required: "Assembly Required",
            self.style: "Style",
            self.water_resistant: "Water Resistant",
            self.upholstery_material: "Upholstery Material",
            self.size: "Size",
            self.gender: "Gender",
            self.fabric_type: "Fabric Type",
            self.washing_instructions: "Washing Instructions",
            self.shoe_type: "Shoe Type",
            self.closure_type: "Closure Type",
            self.fuel_type: "Fuel Type",
            self.transmission: "Transmission",
            self.mileage: "Mileage",
            self.engine_capacity: "Engine Capacity",
            self.top_speed: "Top Speed",
            self.number_of_seats: "Number of Seats",
            self.expiration_date: "Expiration Date",
            self.ingredients: "Ingredients",
            self.calories: "Calories",
            self.dietary_info: "Dietary Info",
            self.package_size: "Package Size",
            self.author: "Author",
            self.publisher: "Publisher",
            self.edition: "Edition",
            self.pages: "Pages",
            self.language: "Language",
            self.paper_type: "Paper Type",
            self.recommended_age: "Recommended Age",
            self.number_of_pieces: "Number of Pieces",
            self.safety_certifications: "Safety Certifications",
            self.battery_required: "Battery Required",
            self.interactive_features: "Interactive Features",
            self.skin_type: "Skin Type",
            self.scent: "Scent",
            self.application_method: "Application Method",
            self.volume: "Volume",
            self.sport_type: "Sport Type",
            self.weather_resistant: "Weather Resistant",
            self.material_durability: "Material Durability",
            self.gemstone: "Gemstone",
            self.metal_type: "Metal Type",
            self.certification: "Certification",
        }

        return {label: value for value, label in details.items() if value not in [None, "", "N/A", "Unknown", "0"]}

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s cart - {self.product.name}"        

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """ Automatically calculate total price before saving """
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"




