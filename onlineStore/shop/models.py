from django.contrib.auth.models import User
from django.db import models


def product_preview_directory_path(instance: 'Product', filename: str) -> str:
    return 'products/product_{pk}/preview/{filename}'.format(pk=instance.pk, filename=filename)


class Product(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    count = models.IntegerField(default=10)
    image = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    customers = models.ManyToManyField(User, related_name='cart')
