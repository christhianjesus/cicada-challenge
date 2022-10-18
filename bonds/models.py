from django.db import models

class Bond(models.Model):
    owner = models.ForeignKey('auth.User', related_name='bounds_for_sale', on_delete=models.CASCADE)
    buyer = models.ForeignKey('auth.User', related_name='purchased_bounds', on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=13, decimal_places=4)
    created = models.DateTimeField(auto_now_add=True)
    bought = models.DateTimeField(auto_now=True)
