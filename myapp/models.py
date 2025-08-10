from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import time
import random
import string
from datetime import timedelta

# Import the password reset model from separate file
from .models_password_reset import PasswordResetCode

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
    phone_number = models.CharField(max_length=15, blank=True, help_text="WhatsApp number used for account recovery")
    area_of_residence = models.CharField(max_length=100, blank=True)
    use_whatsapp_for_recovery = models.BooleanField(default=True, help_text="Use WhatsApp as primary recovery method")
    
    def get_recovery_contact(self):
        """Return the primary recovery contact (WhatsApp if enabled, otherwise email)"""
        if self.use_whatsapp_for_recovery and self.phone_number:
            return self.phone_number
        return self.user.email
    
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
    likes_count = models.PositiveIntegerField(default=0)
    dislikes_count = models.PositiveIntegerField(default=0)

    # General technical details
    condition = models.CharField(max_length=100, default="New", blank=True)
    dimensions = models.CharField(max_length=100, default="", blank=True)
    weight = models.CharField(max_length=50, default="", blank=True)
    material = models.CharField(max_length=100, default="", blank=True)
    color = models.TextField(default="", blank=True)
    warranty = models.CharField(max_length=50, default="No Warranty", blank=True)
    model = models.TextField(default="", blank=True)
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
    processor = models.TextField(default="", blank=True)
    storage_capacity = models.TextField(default="", blank=True)
    screen_size = models.CharField(max_length=50, default="", blank=True)
    resolution = models.TextField(default="", blank=True)

    # Furniture & Home Decor
    weight_capacity = models.CharField(max_length=50, default="", blank=True)
    assembly_required = models.BooleanField(default=None, blank=True, null=True)
    style = models.CharField(max_length=100, default="", blank=True)
    water_resistant = models.BooleanField(default=None, blank=True, null=True)
    upholstery_material = models.CharField(max_length=100, default="", blank=True)

    # Clothing, Shoes & Fashion
    size = models.CharField(max_length=50, default="", blank=True)
    gender = models.CharField(max_length=50, default="", blank=True)
    fabric_type = models.TextField(default="", blank=True)
    washing_instructions = models.TextField(default="", blank=True)
    shoe_type = models.TextField(default="", blank=True)
    closure_type = models.TextField(default="", blank=True)

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
    publisher = models.TextField(default="", blank=True)
    edition = models.CharField(max_length=50, default="", blank=True)
    pages = models.IntegerField(default=None, blank=True, null=True)
    language = models.CharField(max_length=50, default="", blank=True)
    paper_type = models.TextField(default="", blank=True)

    # Toys & Games
    recommended_age = models.CharField(max_length=50, default="", blank=True)
    number_of_pieces = models.IntegerField(default=None, blank=True, null=True)
    safety_certifications = models.TextField(default="", blank=True)
    battery_required = models.BooleanField(default=None, blank=True, null=True)
    interactive_features = models.TextField(default="", blank=True)

    # Health & Beauty
    skin_type = models.CharField(max_length=100, default="", blank=True)
    scent = models.CharField(max_length=100, default="", blank=True)
    application_method = models.TextField(default="", blank=True)
    volume = models.CharField(max_length=50, default="", blank=True)

    # Sports & Outdoor
    sport_type = models.CharField(max_length=100, default="", blank=True)
    weather_resistant = models.BooleanField(default="", blank=True, null=True)
    material_durability = models.TextField(default="", blank=True)

    # Jewelry & Accessories
    gemstone = models.TextField(default="", blank=True)
    metal_type = models.TextField(default="", blank=True)
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

        # Filter out empty values while handling both CharField and TextField types
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
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    
    def update_total(self):
        """Calculate total price from order items"""
        self.total_price = sum(item.price * item.quantity for item in self.items.all())
        self.save()

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def total(self):
        return self.price * self.quantity

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
    chairperson_signature = models.ImageField(upload_to='signatures/', blank=True, null=True)  # Made optional
    chairperson_stamp = models.ImageField(upload_to='stamps/', blank=True, null=True)  # Made optional

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
    worker_signature = models.ImageField(upload_to='signatures/', blank=True, null=True)  # Made optional
    lawyer_name = models.CharField(max_length=255)
    lawyer_signature = models.ImageField(upload_to='signatures/', blank=True, null=True)  # Made optional
    lawyer_stamp = models.ImageField(upload_to='stamps/', blank=True, null=True)  # Made optional
    ceo_name = models.CharField(max_length=255)
    ceo_signature = models.ImageField(upload_to='signatures/', blank=True, null=True)  # Made optional
    ceo_stamp = models.ImageField(upload_to='stamps/', blank=True, null=True)  # Made optional

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
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, null=True, blank=True)
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

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Payment Approved'),
        ('REJECTED', 'Payment Rejected')
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_proof = models.FileField(upload_to='payment_proofs/')
    lipa_number = models.CharField(max_length=50)  # The number where payment was sent to
    reference_number = models.CharField(max_length=100)  # Payment reference provided by user
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_payments')
    notes = models.TextField(blank=True)
    seller_reviewed = models.BooleanField(default=False, help_text="Whether the seller has reviewed this payment")
    seller_approval = models.BooleanField(null=True, blank=True, help_text="Seller's decision on payment approval")
    seller_notes = models.TextField(blank=True, help_text="Seller's notes on the payment")
    seller_reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status} - {self.amount}"

    def approve_payment(self, admin_user):
        from django.utils import timezone
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            # Update payment status
            self.status = 'APPROVED'
            self.approved_at = timezone.now()
            self.approved_by = admin_user
            self.save()

            # Generate receipt
            from .models import Receipt
            receipt, created = Receipt.objects.get_or_create(
                payment=self,
                defaults={
                    'order': self.order,
                    'transaction_id': f"PAY-{self.id}"
                }
            )

            # Send emails asynchronously if possible
            try:
                # Try to use Django's background tasks
                from django.db import transaction
                from .tasks import send_payment_approved_emails
                
                # Call the task outside the current transaction to prevent blocking
                transaction.on_commit(lambda: send_payment_approved_emails(self.id))
                logger.info(f"Email sending task queued for payment {self.id}")
            except ImportError:
                # If background task processing is not available, send emails directly
                from .tasks import send_payment_approved_emails
                send_payment_approved_emails(self.id)
                logger.info(f"Emails sent synchronously for payment {self.id}")
                
            return True
        except Exception as e:
            logger.error(f"Error in approve_payment: {str(e)}")
            # Re-raise the exception to show error in admin
            raise
            
    def reject_payment(self, user, reason=""):
        from django.utils import timezone
        
        self.status = 'REJECTED'
        self.approved_at = timezone.now()
        self.approved_by = user
        self.notes = reason
        self.save()
        
        # TODO: Implement email notification for payment rejection
        
    def get_seller(self):
        """Return the seller associated with this payment's order items"""
        # Get first order item's product seller
        order_items = self.order.items.all()
        if order_items.exists():
            first_item = order_items.first()
            return first_item.product.seller
        return None


class AdminMessage(models.Model):
    message = models.TextField(help_text="Enter the message to be displayed to users")
    title = models.CharField(max_length=255, blank=True, null=True, help_text="Optional title for the message")
    start_date = models.DateTimeField(help_text="When this message should start showing")
    end_date = models.DateTimeField(help_text="When this message should stop showing")
    is_active = models.BooleanField(default=True, help_text="Manually disable the message if needed")
    position = models.CharField(max_length=10, choices=[('left', 'Left'), ('right', 'Right')], 
                               default='right', help_text="Which side of the screen to show the message on")
    priority = models.IntegerField(default=0, help_text="Higher priority messages show on top if multiple are active")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority', '-start_date']
        
    def __str__(self):
        return f"{self.title or 'Message'} ({self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')})"
    
    def is_currently_active(self):
        now = timezone.now()
        return (
            self.is_active and 
            self.start_date <= now <= self.end_date
        )



class ProductInteraction(models.Model):
    LIKE = 'LIKE'
    DISLIKE = 'DISLIKE'
    INTERACTION_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Ensure a user can only have one interaction per product
        unique_together = ('user', 'product')
        
    def __str__(self):
        return f"{self.user.username} - {self.interaction_type} - {self.product.name}"
