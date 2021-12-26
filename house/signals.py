from django.db.models.signals import post_save
from django.dispatch import receiver

from house.models import House
from house.tasks import find_house


@receiver(post_save, sender=House)
def post_save_generate_code(sender, instance=None, created=False, **kwargs):
    if created:
        find_house.delay(pk=instance.pk, region=instance.region, city=instance.city,
                         street=instance.street, number=instance.number)