from django.db import models

from hybeta.models.soft_delete import SoftDeleteModel


class District:
    WAN_CHAI = "WC"
    CENTRAL_AND_WESTERN = "CW"
    SAI_KUNG = "SK"
    EASTERN = "E"
    SOUTHERN = "S"
    TSUEN_WAN = "TW"
    NORTH = "N"
    KOWLOON_CITY = "KC"
    YAU_TSIM_MONG = "YTM"
    SHA_TIN = "ST"
    ISLANDS = "I"
    YUEN_LONG = "YL"
    TAI_PO = "TP"
    WONG_TAI_SIN = "WTS"
    TUEN_MUN = "TM"
    KWAI_TSING = "KTS"
    SHAM_SHUI_PO = "SSP"
    KWUN_TONG = "KT"

    CHOICES = (
        (WAN_CHAI, "Wan Chai"),
        (CENTRAL_AND_WESTERN, "Central and Western"),
        (SAI_KUNG, "Sai Kung"),
        (EASTERN, "Eastern"),
        (SOUTHERN, "Southern"),
        (TSUEN_WAN, "Tsuen Wan"),
        (NORTH, "North"),
        (KOWLOON_CITY, "Kowloon City"),
        (YAU_TSIM_MONG, "Yau Tsim Mong"),
        (SHA_TIN, "Sha Tin"),
        (ISLANDS, "Islands"),
        (YUEN_LONG, "Yuen Long"),
        (TAI_PO, "Tai Po"),
        (WONG_TAI_SIN, "Wong Tai Sin"),
        (TUEN_MUN, "Tuen Mun"),
        (KWAI_TSING, "Kwai Tsing"),
        (SHAM_SHUI_PO, "Sham Shui Po"),
        (KWUN_TONG, "Kwun Tong"),
    )


class Location(SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    district = models.CharField(null=False, max_length=3, choices=District.CHOICES, db_index=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    name = models.TextField(null=True)

    class Meta:
        db_table = "hybeta_location"
        verbose_name = "hybeta_location"
        verbose_name_plural = "hybeta_locations"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.id} | {self.name} | {self.district}"
