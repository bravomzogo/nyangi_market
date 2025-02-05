from django import forms
from django.contrib.auth.models import User
from .models import Seller, Product

class SellerRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Seller
        fields = ['shop_name', 'product_types']

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
        fields = ['name', 'description', 'price',  'image','category']
