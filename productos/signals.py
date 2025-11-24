from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Product


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(pre_save, sender=Product)
def auto_deactivate_product_without_stock(sender, instance, **kwargs):
    """Desactiva automáticamente productos sin stock"""
    if instance.stock == 0:
        instance.is_active = False
    elif instance.stock > 0 and not instance.pk:  # Nuevo producto con stock
        instance.is_active = True
