from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, Tech, CustomUser  # Ensure CustomUser is defined in models.py

# ProductForm: No changes needed here, assuming Product model exists
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'description', 'image', 'image1', 'image2', 'image3', 'image4', 'stock', 'location']

# TechForm: Corrected indentation and removed unnecessary widgets/labels duplication
class TechForm(forms.ModelForm):
    class Meta:
        model = Tech
        fields = [
            'condition', 'dimensions', 'weight', 'material', 'color', 'warranty', 'model', 'release_year',
            'generation', 'brand', 'origin_country', 'power_consumption', 'battery_life', 'charging_time',
            'connectivity', 'processor', 'storage_capacity', 'screen_size', 'resolution', 'weight_capacity',
            'assembly_required', 'style', 'water_resistant', 'upholstery_material', 'size', 'gender', 'fabric_type',
            'washing_instructions', 'shoe_type', 'closure_type', 'fuel_type', 'transmission', 'mileage',
            'engine_capacity', 'top_speed', 'number_of_seats', 'expiration_date', 'ingredients', 'calories',
            'dietary_info', 'package_size', 'author', 'publisher', 'edition', 'pages', 'language', 'paper_type',
            'recommended_age', 'safety_certifications', 'battery_required', 'interactive_features',
            'skin_type', 'scent', 'application_method', 'volume', 'sport_type', 'weather_resistant',
            'material_durability', 'gemstone', 'metal_type', 'certification'
        ]

    widgets = {
        'condition': forms.Select(choices=[("New", "New"), ("Used", "Used"), ("Refurbished", "Refurbished")]),
        'dimensions': forms.TextInput(attrs={'placeholder': 'L x W x H'}),
        'weight': forms.TextInput(attrs={'placeholder': 'e.g., 1.5kg, 500g'}),
        'material': forms.TextInput(attrs={'placeholder': 'Plastic, Metal, Leather'}),
        'color': forms.TextInput(attrs={'placeholder': 'Black, Red, Blue'}),
        'warranty': forms.TextInput(attrs={'placeholder': '6 months, 1 year'}),
        'release_year': forms.NumberInput(attrs={'min': 1900, 'max': 2025}),
        'brand': forms.TextInput(attrs={'placeholder': 'Brand Name'}),
        'origin_country': forms.TextInput(attrs={'placeholder': 'Country of manufacture'}),
        'power_consumption': forms.TextInput(attrs={'placeholder': 'e.g., 100W, 220V'}),
        'battery_life': forms.TextInput(attrs={'placeholder': 'e.g., 10 hours'}),
        'charging_time': forms.TextInput(attrs={'placeholder': 'e.g., 2 hours'}),
        'connectivity': forms.TextInput(attrs={'placeholder': 'Wi-Fi, Bluetooth, 4G'}),
        'processor': forms.TextInput(attrs={'placeholder': 'Snapdragon, Intel i7'}),
        'storage_capacity': forms.TextInput(attrs={'placeholder': 'e.g., 256GB SSD'}),
        'screen_size': forms.TextInput(attrs={'placeholder': 'e.g., 15.6 inches'}),
        'resolution': forms.TextInput(attrs={'placeholder': '1080p, 4K, 720p'}),
        'weight_capacity': forms.TextInput(attrs={'placeholder': 'e.g., 100kg'}),
        'style': forms.TextInput(attrs={'placeholder': 'Modern, Vintage'}),
        'fabric_type': forms.TextInput(attrs={'placeholder': 'Cotton, Wool, Silk'}),
        'shoe_type': forms.TextInput(attrs={'placeholder': 'Sneakers, Boots, Sandals'}),
        'fuel_type': forms.TextInput(attrs={'placeholder': 'Petrol, Diesel, Electric'}),
        'mileage': forms.TextInput(attrs={'placeholder': 'e.g., 20km/l'}),
        'engine_capacity': forms.TextInput(attrs={'placeholder': 'e.g., 2000cc'}),
        'top_speed': forms.TextInput(attrs={'placeholder': 'e.g., 220 km/h'}),
        'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        'ingredients': forms.Textarea(attrs={'placeholder': 'List of ingredients'}),
        'calories': forms.TextInput(attrs={'placeholder': 'e.g., 200 kcal per serving'}),
        'author': forms.TextInput(attrs={'placeholder': 'Author Name'}),
        'publisher': forms.TextInput(attrs={'placeholder': 'Publisher Name'}),
        'edition': forms.TextInput(attrs={'placeholder': '1st, 2nd Edition'}),
        'pages': forms.NumberInput(attrs={'min': 1}),
        'language': forms.TextInput(attrs={'placeholder': 'English, French, etc.'}),
        'recommended_age': forms.TextInput(attrs={'placeholder': '3+, 12+'}),
        'safety_certifications': forms.TextInput(attrs={'placeholder': 'ASTM, CE Certified'}),
        'skin_type': forms.TextInput(attrs={'placeholder': 'Dry, Oily, Normal'}),
        'scent': forms.TextInput(attrs={'placeholder': 'Floral, Citrus, Woody'}),
        'application_method': forms.TextInput(attrs={'placeholder': 'Spray, Cream, Gel'}),
        'volume': forms.TextInput(attrs={'placeholder': '500ml, 100g'}),
        'sport_type': forms.TextInput(attrs={'placeholder': 'Football, Basketball'}),
        'material_durability': forms.TextInput(attrs={'placeholder': 'High Impact Plastic'}),
        'gemstone': forms.TextInput(attrs={'placeholder': 'Diamond, Ruby, Sapphire'}),
        'metal_type': forms.TextInput(attrs={'placeholder': 'Gold, Silver, Platinum'}),
        'certification': forms.TextInput(attrs={'placeholder': 'Certified Gemstone'}),
    }

# CustomUserCreationForm: Fixed Meta class and ensured user_type is handled
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define choices for user_type (assuming it's a CharField with choices in the model)
        self.fields['user_type'].choices = [
            ('STAFF', 'Staff'),
            ('CUSTOMER', 'Customer'),
        ]
        # Add placeholders and classes
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter your username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email address'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter your password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm your password'})
        self.fields['user_type'].widget.attrs.update({'class': 'form-select'})

# CustomAuthenticationForm: Removed unnecessary Meta class
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter your username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter your password'})