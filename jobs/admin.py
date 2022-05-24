from django.contrib import admin

from hybeta.services.utils import Utils
from jobs.models import Doctor, DoctorTranslation, Location

UTIL_FIELDS = Utils.get_util_fields()


class DoctorAdmin(admin.ModelAdmin):
    exclude = UTIL_FIELDS


class DoctorTranslationAdmin(admin.ModelAdmin):
    exclude = UTIL_FIELDS


class LocationAdmin(admin.ModelAdmin):
    exclude = UTIL_FIELDS


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(DoctorTranslation, DoctorTranslationAdmin)
admin.site.register(Location, LocationAdmin)
