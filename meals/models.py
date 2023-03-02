from django.db import models

from mainsite.models import City, ZipCode
from mainsite.helpers import get_lat_long


class Route(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Stop(models.Model):
    TYPE_CHOICE_HOT = 'hot'
    TYPE_CHOICE_COLD = 'cold'
    TYPE_CHOICES = (
        (TYPE_CHOICE_HOT, "hot"),
        (TYPE_CHOICE_COLD, "cold")
    )
    
    class Meta:
        ordering = ["address"]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True)
    longitude = models.DecimalField(
        max_digits=10, decimal_places=7, blank=True
    )
    meal_type = models.CharField(
        max_length=4, choices=TYPE_CHOICES, default=TYPE_CHOICE_HOT, blank=True
    )
    waitlist = models.BooleanField(default=False)
    phone = models.CharField(max_length=100)
    phone_notes = models.CharField(max_length=300, blank=True)
    notes = models.CharField(max_length=300)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.latitude and not self.longitude:
            self.latitude, self.longitude = get_lat_long(
                self.address, self.city.name, self.city.state.name,
                self.zip_code.code
            )
            if not self.latitude:
                self.latitude = 0
            if not self.longitude:
                self.longitude = 0
        super().save(*args, **kwargs)
