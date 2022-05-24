class DoctorCategory:
    GENERAL_PRACTITIONER = "GP"
    DENTISTRY = "D"
    CARDIOLOGY = "C"
    FAMILY = "F"
    KID = "K"

    CHOICES = (
        (GENERAL_PRACTITIONER, "General Practitioner"),
        (DENTISTRY, "Dentistry"),
        (CARDIOLOGY, "Cardiology"),
        (FAMILY, "Family"),
        (KID, "Kid"),
    )


class Language:
    ENGLISH = "EN"
    HONG_KONG = "HK"

    CHOICES = (
        (ENGLISH, "English"),
        (HONG_KONG, "Hong Kong"),
    )
