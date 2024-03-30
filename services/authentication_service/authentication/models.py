from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver 
from django.db.models.signals import post_save
import uuid

class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    email_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.png')
    subscription_plan = models.CharField(max_length=255, default='Free')
    otp = models.IntegerField(default=0)
    otp_created_at = models.DateTimeField(auto_now_add=True)
    accept_terms = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=50,default="",blank=True)
    reset_password_expire = models.DateTimeField(null=True,blank=True)
    
@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    else:
        # For existing users without a profile, create one
        if not hasattr(instance, 'profile'):
            Profile.objects.get_or_create(user=instance)
            
