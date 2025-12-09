from django.db import models
from django.contrib.auth.models import User
import random
from django.utils import timezone

class Documentation(models.Model):
    file_name = models.CharField(max_length=255)
    language = models.CharField(max_length=50)
    code = models.TextField()
    generated_doc = models.JSONField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        """Generate a new 6-digit OTP and update the timestamp."""
        self.code = str(random.randint(100000, 999999))
        self.created_at = timezone.now()
        self.save()

    def is_valid(self):
        """Check if OTP is still valid (e.g., within 5 minutes)."""
        return (timezone.now() - self.created_at).seconds < 300  

    def __str__(self):
        return f"OTP for {self.user.username}"
