from django.db import models
from django.utils.translation import gettext as _


class Tag(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(_("name"), max_length=200)


class Responsibility(models.Model):
    class Meta:
        verbose_name = _("Responsibility")
        verbose_name_plural = _("Responsibilities")
        ordering = ["name"]
    
    def __str__(self):
        return self.name

    name = models.CharField(_("name"), max_length=500)
    description = models.CharField(_("description"), max_length=500, blank=True)
    link = models.URLField(_("link"), blank=True)
    tags = models.ManyToManyField(Tag)
    primary_employee = models.ForeignKey("people.Employee", related_name="primary_responsibilities", null=True, on_delete=models.SET_NULL)
    secondary_employee = models.ForeignKey("people.Employee", related_name="secondary_responsibilities", null=True, on_delete=models.SET_NULL)


