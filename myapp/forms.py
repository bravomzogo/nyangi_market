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
        fields = ['name', 'description', 'price', 'category', 'image', 'image1', 'image2', 'image3', 'image4', 'release_year', 'video']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter product description'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter price in your currency'}),
            'category': forms.Select(),
            'release_year': forms.NumberInput(attrs={'placeholder': 'Enter release year (optional)', 'min': 1900, 'max': 2100}),
            'video': forms.ClearableFileInput(attrs={'accept': 'video/*'}),
        }
        labels = {
            'name': "Product Name",
            'description': "Product Description",
            'price': "Price",
            'category': "Category",
            'image': "Main Image",
            'release_year': "Release Year",
            'video': "Product Video",
        }

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
            'chairperson_name', 'chairperson_post',  # Removed signature and stamp fields
            'nida_passport_doc', 'driving_license_doc', 'police_clearance_doc', 'educational_certificates_doc',
            'contract_rules',  # Removed worker_signature
            'lawyer_name',  # Removed lawyer_signature and stamp
            'ceo_name',  # Removed ceo_signature and stamp
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

