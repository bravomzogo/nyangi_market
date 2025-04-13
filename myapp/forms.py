from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Seller, Product, WorkerContract, ParentDetails, Referee, EducationRecord, SubscriptionPlan, SellerSubscription


class CustomUserRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True, help_text="Enter your phone number.")
    area_of_residence = forms.CharField(max_length=100, required=True, help_text="Enter your area of residence.")

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'area_of_residence', 'password1', 'password2']


class SellerRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Seller
        fields = ['shop_name']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        seller = super().save(commit=False)
        seller.user = user
        if commit:
            seller.save()
        return seller

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'category', 'image', 'image1', 'image2', 'image3','phone_number', 'image4', 'location',
            'condition', 'dimensions', 'weight', 'material', 'color', 'warranty', 'model', 'release_year',
            'generation', 'brand', 'origin_country', 'power_consumption', 'battery_life', 'charging_time',
            'connectivity', 'processor', 'storage_capacity', 'screen_size', 'resolution', 'weight_capacity',
            'assembly_required', 'style', 'water_resistant', 'upholstery_material', 'size', 'gender', 'fabric_type',
            'washing_instructions', 'shoe_type', 'closure_type', 'fuel_type', 'transmission', 'mileage',
            'engine_capacity', 'top_speed', 'number_of_seats', 'expiration_date', 'ingredients', 'calories',
            'dietary_info', 'package_size', 'author', 'publisher', 'edition', 'pages', 'language', 'paper_type',
            'recommended_age', 'number_of_pieces', 'safety_certifications', 'battery_required', 'interactive_features',
            'skin_type', 'scent', 'application_method', 'volume', 'sport_type', 'weather_resistant',
            'material_durability', 'gemstone', 'metal_type', 'certification'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter product description'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter price in your currency'}),
            'category': forms.Select(),
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
            'number_of_pieces': forms.NumberInput(attrs={'min': 1}),
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

        labels = {
            'image':"Main Image",
            'name': "Product Name",
            'description': "Product Description",
            'price': "Price",
            'category': "Category",
            'location': "Location",
            'condition': "Condition",
            'dimensions': "Dimensions (L x W x H)",
            'weight': "Weight",
            'warranty': "Warranty Period",
            'release_year': "Year of Release",
            'brand': "Brand Name",
            'origin_country': "Country of Origin",
            'power_consumption': "Power Consumption",
            'battery_life': "Battery Life",
            'charging_time': "Charging Time",
            'connectivity': "Connectivity Options",
            'processor': "Processor Type",
            'storage_capacity': "Storage Capacity",
            'screen_size': "Screen Size (in inches)",
            'resolution': "Screen Resolution",
            'style': "Furniture Style",
            'fabric_type': "Fabric Type",
            'shoe_type': "Shoe Type",
            'fuel_type': "Fuel Type",
            'mileage': "Mileage",
            'engine_capacity': "Engine Capacity",
            'top_speed': "Top Speed",
            'expiration_date': "Expiration Date",
            'ingredients': "List of Ingredients",
            'calories': "Calories per Serving",
            'author': "Book Author",
            'publisher': "Book Publisher",
            'edition': "Book Edition",
            'pages': "Number of Pages",
            'language': "Book Language",
            'recommended_age': "Recommended Age Group",
            'number_of_pieces': "Number of Pieces",
            'safety_certifications': "Safety Certifications",
            'skin_type': "Suitable for Skin Type",
            'scent': "Scent Type",
            'application_method': "Application Method",
            'volume': "Volume/Weight",
            'sport_type': "Sport Type",
            'material_durability': "Material Durability",
            'gemstone': "Gemstone Type",
            'metal_type': "Metal Type",
            'certification': "Certification Type",
        }


    # Add location dropdown

class ParentDetailsForm(forms.ModelForm):
    class Meta:
        model = ParentDetails
        fields = ['first_name', 'second_name', 'residence', 'is_mother']

class RefereeForm(forms.ModelForm):
    class Meta:
        model = Referee
        fields = ['name', 'occupation', 'signature']

class EducationRecordForm(forms.ModelForm):
    class Meta:
        model = EducationRecord
        fields = ['primary', 'secondary', 'high_school', 'university', 'talents']

class WorkerContractForm(forms.ModelForm):
    class Meta:
        model = WorkerContract
        fields = [
            'first_name', 'second_name', 'third_name', 'sex', 'marital_status', 'spouse_details',
            'nationality', 'passport_nida', 'date_of_birth', 'drivers_license',
            'present_address', 'permanent_address', 'phone_number', 'whatsapp_number',
            'chairperson_name', 'chairperson_post', 'chairperson_signature', 'chairperson_stamp',
            'nida_passport_doc', 'driving_license_doc', 'police_clearance_doc', 'educational_certificates_doc',
            'contract_rules', 'worker_signature', 'lawyer_name', 'lawyer_signature', 'lawyer_stamp',
            'ceo_name', 'ceo_signature', 'ceo_stamp'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'contract_rules': forms.Textarea(attrs={'rows': 10}),
            'spouse_details': forms.Textarea(attrs={'rows': 3}),
        }

class SubscriptionPlanForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = ['name', 'description', 'price', 'duration_days', 'features', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'features': forms.Textarea(attrs={'rows': 5}),
        }

class SellerSubscriptionForm(forms.ModelForm):
    class Meta:
        model = SellerSubscription
        fields = ['plan', 'level', 'auto_renew']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plan'].queryset = SubscriptionPlan.objects.filter(is_active=True)

