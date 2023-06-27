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


class State(models.Model):
    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("States")

    def __str__(self):
        return self.name

    name = models.CharField(_("name"), max_length=255)


class ZipCode(models.Model):
    class Meta: 
        verbose_name = _("Zip Code")
        verbose_name_plural = _("Zip Codes")

    def __str__(self):
        return self.code

    code = models.CharField(_("code"), max_length=5)
    

class City(models.Model):
    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")

    def __str__(self):
        return self.name

    name = models.CharField(_("name"), max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)



LANGUAGE_CHOICES = (
    ("asl", _("American Sign Language")),
    ("ar", _("Arabic")),
    ("bn", _("Bengali")),
    ("zh", _("Chinese")),
    ("hr", _("Croatian")),
    ("cs", _("Czech")),
    ("da", _("Danish")),
    ("nl", _("Dutch")),
    ("fi", _("Finnish")),
    ("fr", _("French")),
    ("de", _("German")),
    ("el", _("Greek")),
    ("gu", _("Gujarati")),
    ("ht", _("Haitian Creole")),
    ("he", _("Hebrew")),
    ("hi", _("Hindi")),
    ("hu", _("Hungarian")),
    ("id", _("Indonesian")),
    ("it", _("Italian")),
    ("ja", _("Japanese")),
    ("ko", _("Korean")),
    ("lv", _("Latvian")),
    ("lt", _("Lithuanian")),
    ("no", _("Norwegian")),
    ("fa", _("Persian")),
    ("pl", _("Polish")),
    ("pt", _("Portuguese")),
    ("ro", _("Romanian")),
    ("ru", _("Russian")),
    ("sr", _("Serbian")),
    ("sk", _("Slovak")),
    ("sl", _("Slovenian")),
    ("es", _("Spanish")),
    ("sw", _("Swahili")),
    ("sv", _("Swedish")),
    ("tl", _("Tagalog")),
    ("ta", _("Tamil")),
    ("th", _("Thai")),
    ("tr", _("Turkish")),
    ("ur", _("Urdu")),
    ("vi", _("Vietnamese")),
    ("cy", _("Welsh")),
    ("xh", _("Xhosa")),
    ("zu", _("Zulu")),
)