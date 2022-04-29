from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from ckeditor.fields import RichTextField


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class ImageUpload(models.Model):
    description = models.CharField(_("description"), max_length=255)
    image = models.ImageField(upload_to="uploads/image-upload")


class SecurityMessage(models.Model):
    class Meta:
        verbose_name = _("Security Message")
        verbose_name_plural = _("Security Messages")
        ordering = ["active", "-pk"]
        get_latest_by = ("date")

    active = models.BooleanField(default=False)
    description = models.CharField(_("description"), max_length=255)
    date = models.DateField(default=timezone.now)
    content = RichTextField()

    def __str__(self):
        return self.description


class TrustedIPAddress(models.Model):
    """
    Allow these addresses to access the Desk Reservation App
    """
    
    class Meta:
        verbose_name = _("Trusted IP Address")
        verbose_name_plural = _("Trusted IP Addresses")

    def __str__(self):
        return _("Trusted IP Address")

    address = models.GenericIPAddressField()
    description = models.CharField(max_length=255)
    