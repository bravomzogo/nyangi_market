import random
import string
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User

class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Allow longer codes (e.g. 8 chars or more) to support alphanumeric codes
    code = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = ''.join(random.choices(string.digits, k=6))
        
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=15)
            
        super().save(*args, **kwargs)
    
    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()
