from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Bond(models.Model):
    owner = models.ForeignKey('auth.User', related_name='bounds_for_sale', on_delete=models.CASCADE)
    buyer = models.ForeignKey('auth.User', related_name='purchased_bounds', on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=13, decimal_places=4)
    created = models.DateTimeField(auto_now_add=True)
    bought = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)