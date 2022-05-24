from django.db import models

from hybeta.const import DoctorCategory, Language
from hybeta.models import AutoTimeStampedModel, SoftDeleteModel
from jobs.models import Location


class Doctor(AutoTimeStampedModel, SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=20, default="", null=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, null=False)
    category = models.CharField(null=False, max_length=20, choices=DoctorCategory.CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available_time = models.TextField(null=True)

    class Meta:
        db_table = "hybeta_doctor"
        verbose_name = "hybeta_doctor"
        verbose_name_plural = "hybeta_doctors"
        ordering = ["-id"]
        index_together = [("category", "price")]

    def __str__(self):
        return f"{self.id} | {self.category} | {self.phone}"


# TODO https://github.com/KristianOellegaard/django-hvad may handle better
class DoctorTranslation(AutoTimeStampedModel, SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, null=False, related_name="doctor_translations")
    language_code = models.CharField(null=False, max_length=20, choices=Language.CHOICES)
    name = models.CharField(max_length=255, default="")
    note = models.TextField(null=True)

    class Meta:
        db_table = "hybeta_doctor_translation"
        verbose_name = "hybeta_doctor_translation"
        verbose_name_plural = "hybeta_doctor_translations"
        ordering = ["-id"]
        index_together = (("doctor", "language_code"),)

    def __str__(self):
        return f"lang: {self.language_code} | #{self.id} | doctor_id: {self.doctor} | name: {self.name}"
