from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_approved = models.BooleanField(default=False)


class Sheet(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    gem = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    place = models.CharField(max_length=100, blank=True, null=True)
    officer = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    marketing = models.CharField(max_length=100, blank=True, null=True)

    item = models.CharField(max_length=100, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    gst = models.FloatField(blank=True, null=True)

    company = models.CharField(max_length=100, blank=True, null=True)
    bill = models.CharField(max_length=50, blank=True, null=True)
    billdate = models.DateField(blank=True, null=True)

    qty = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)

    fr = models.FloatField(blank=True, null=True)
    fb = models.FloatField(blank=True, null=True)
    tfr = models.FloatField(blank=True, null=True)

    orderby = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Sheet"
        verbose_name_plural = "Sheets"

    def save(self, *args, **kwargs):

        try:
            self.qty = float(self.qty or 0)
            self.price = float(self.price or 0)
            self.gst = float(self.gst or 0)

            subtotal = self.qty * self.price
            gst_amount = subtotal * (self.gst / 100)

            self.amount = subtotal + gst_amount

        except (ValueError, TypeError):
            self.amount = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item or 'No Item'} - {self.user.username}"