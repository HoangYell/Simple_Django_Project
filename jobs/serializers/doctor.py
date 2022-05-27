from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from hybeta.services.utils import Utils
from jobs.models import Doctor, DoctorTranslation, Location


class DoctorTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorTranslation
        exclude = (*Utils.get_util_fields(), "doctor")


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = Utils.get_soft_delete_fields()

    def get_attribute(self, instance):
        # FORMAT doctor.location in list_serialize
        # set null if location not satisfy the params_2_queryset
        location_queryset = Utils.params_2_queryset(Location, self.context, mandatory_filter=dict(id=instance.location_id))
        if location_queryset.exists():
            return super().get_attribute(instance)


class DoctorSerializer(serializers.ModelSerializer):
    doctor_translations = serializers.SerializerMethodField()
    location = LocationSerializer()

    class Meta:
        class DoctorListSerializer(serializers.ListSerializer):
            def to_representation(self, data):
                results = super().to_representation(data)
                return [result for result in results if result["doctor_translations"] and result["location"]]

        model = Doctor
        exclude = Utils.get_util_fields()
        # list_serializer: use DoctorListSerializer instead of DoctorSerializer
        # DoctorListSerializer.to_representation will remove doctor, who have flag = None or []
        # from steps: (FORMAT doctor.location, FORMAT doctor.doctor_translations)
        list_serializer_class = DoctorListSerializer

    def get_doctor_translations(self, obj):
        # FORMAT doctor.doctor_translations in list_serialize
        # set [] if doctor_translations not satisfy the params_2_queryset
        doctor_translation_queryset = Utils.params_2_queryset(DoctorTranslation, self.context, mandatory_filter=dict(doctor_id=obj.id))
        serializer = DoctorTranslationSerializer(doctor_translation_queryset, many=True)
        return serializer.data


class DoctorCreateSerializer(DoctorSerializer):
    doctor_translations = DoctorTranslationSerializer(many=True, required=False)

    def validate(self, value):
        # TODO validate in here
        _doctor_translations = value.get("doctor_translations")
        doctor_translations_valid = _doctor_translations and isinstance(_doctor_translations, list)
        if not doctor_translations_valid:
            raise ValidationError(f"doctor_translations: {_doctor_translations} is invalid!")

        return super().validate(value)

    def create(self, validated_data):
        location_data = validated_data.pop("location")
        doctor_translations_data = validated_data.pop("doctor_translations")
        doctor_data = validated_data

        location_serializer = LocationSerializer(data=location_data)
        if location_serializer.is_valid(raise_exception=True):
            location_instance = location_serializer.save()

            doctor_data["location_id"] = location_instance.id
            doctor_instance = super().create(doctor_data)

            doctor_translation_serializer = DoctorTranslationSerializer(data=doctor_translations_data, many=True)
            if doctor_translation_serializer.is_valid(raise_exception=True):
                doctor_translation_instances = [DoctorTranslation(**doctor_translation_instance, doctor_id=doctor_instance.id) for doctor_translation_instance in doctor_translation_serializer.validated_data]
                DoctorTranslation.objects.bulk_create(doctor_translation_instances, batch_size=100)
        return doctor_instance
