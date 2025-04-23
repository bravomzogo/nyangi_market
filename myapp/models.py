from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import time
import random
import string


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

class ProductAttribute(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    attribute_type = models.CharField(max_length=50, choices=[
        ('text', 'Text'),
        ('number', 'Number'),
        ('select', 'Select'),
        ('boolean', 'Boolean'),
    ])
    required = models.BooleanField(default=False)
    options = models.TextField(blank=True, help_text="For select type, enter options separated by commas")

    def __str__(self):
        return f"{self.name} ({self.category.name})"

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
    assembly_required = models.BooleanField(default=None, blank=True, null=True)
    style = models.CharField(max_length=100, default="", blank=True)
    water_resistant = models.BooleanField(default=None, blank=True, null=True)
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
    number_of_seats = models.IntegerField(default=None, blank=True, null=True)

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
    pages = models.IntegerField(default=None, blank=True, null=True)
    language = models.CharField(max_length=50, default="", blank=True)
    paper_type = models.CharField(max_length=100, default="", blank=True)

    # Toys & Games
    recommended_age = models.CharField(max_length=50, default="", blank=True)
    number_of_pieces = models.IntegerField(default=None, blank=True, null=True)
    safety_certifications = models.CharField(max_length=100, default="", blank=True)
    battery_required = models.BooleanField(default=None, blank=True, null=True)
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

    video = models.FileField(upload_to='product_videos/', null=True, blank=True, default=None)  # Ensure default is None
    attributes = models.JSONField(default=dict, blank=True)  # Store dynamic attributes

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

    def get_attributes_for_category(self):
        if self.category:
            return ProductAttribute.objects.filter(category=self.category)
        return []

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

class ParentDetails(models.Model):
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    residence = models.CharField(max_length=255)
    is_mother = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.second_name}"

class Referee(models.Model):
    name = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    signature = models.ImageField(upload_to='signatures/')

    def __str__(self):
        return self.name

class EducationRecord(models.Model):
    primary = models.CharField(max_length=255)
    secondary = models.CharField(max_length=255)
    high_school = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    talents = models.TextField()

    def __str__(self):
        return f"Education Record - {self.university}"

class WorkerContract(models.Model):
    # Personal Details
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    third_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    marital_status = models.CharField(max_length=20, choices=[
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed')
    ])
    spouse_details = models.TextField(blank=True, null=True)
    nationality = models.CharField(max_length=100)
    passport_nida = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    drivers_license = models.CharField(max_length=50)

    # Parent Details
    father = models.ForeignKey(ParentDetails, on_delete=models.CASCADE, related_name='father_contracts')
    mother = models.ForeignKey(ParentDetails, on_delete=models.CASCADE, related_name='mother_contracts')

    # Address
    present_address = models.TextField()
    permanent_address = models.TextField()
    phone_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15)

    # Referees
    referee1 = models.ForeignKey(Referee, on_delete=models.CASCADE, related_name='referee1_contracts')
    referee2 = models.ForeignKey(Referee, on_delete=models.CASCADE, related_name='referee2_contracts')

    # Street/Ward Chairperson
    chairperson_name = models.CharField(max_length=255)
    chairperson_post = models.CharField(max_length=255)
    chairperson_signature = models.ImageField(upload_to='signatures/')
    chairperson_stamp = models.ImageField(upload_to='stamps/')

    # Education
    education_record = models.ForeignKey(EducationRecord, on_delete=models.CASCADE)

    # Documents
    nida_passport_doc = models.FileField(upload_to='documents/')
    driving_license_doc = models.FileField(upload_to='documents/')
    police_clearance_doc = models.FileField(upload_to='documents/')
    educational_certificates_doc = models.FileField(upload_to='documents/')

    # Contract Rules
    contract_rules = models.TextField()

    # Signatures
    worker_signature = models.ImageField(upload_to='signatures/')
    lawyer_name = models.CharField(max_length=255)
    lawyer_signature = models.ImageField(upload_to='signatures/')
    lawyer_stamp = models.ImageField(upload_to='stamps/')
    ceo_name = models.CharField(max_length=255)
    ceo_signature = models.ImageField(upload_to='signatures/')
    ceo_stamp = models.ImageField(upload_to='stamps/')

    # Status
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.second_name} {self.third_name}"

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    features = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SellerSubscription(models.Model):
    SUBSCRIPTION_LEVELS = [
        ('BRONZE', 'Bronze Booster'),
        ('SILVER', 'Silver Spotlight'),
        ('GOLD', 'Gold Galaxy'),
    ]

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    level = models.CharField(max_length=10, choices=SUBSCRIPTION_LEVELS)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    auto_renew = models.BooleanField(default=True)
    payment_status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.seller.shop_name} - {self.plan.name}"

    def is_valid(self):
        return self.is_active and self.end_date > timezone.now()

class SubscriptionFeature(models.Model):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.plan.name} - {self.name}"

class Receipt(models.Model):
    transaction_id = models.CharField(max_length=50, unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='receipts/', null=True, blank=True)
    
    def generate_transaction_id(self):
        timestamp = int(time.time())
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"NY{timestamp}{random_str}"
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_transaction_id()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Receipt {self.transaction_id}"




