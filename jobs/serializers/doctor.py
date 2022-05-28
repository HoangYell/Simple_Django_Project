from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from hybeta.services.utils import Utils
from jobs.models import Doctor, DoctorTranslation, Location


class DoctorTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorTranslation
        exclude = (*Utils.get_util_fields(), "doctor")


class LocationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)  # equal to super().to_internal_value(data).update(id=location_id)

    class Meta:
        model = Location
        exclude = Utils.get_soft_delete_fields()

    @staticmethod
    def _get_data_from_id(existing_id):
        """
        Handle case: doctor.location = {"id": existing_id}
        :param existing_id: existing location id

        Example:
            :argument:
                location_id = 2,
                data = {'filter_1__location_id': '1', 'sort_1__price': 'desc', 'sort_2__id': 'asc'},
                mandatory_filter = {'pk': '1'}
            :return:
                {
                    "id": 2,
                    "district": "TP",
                    "latitude": "874.1669429",
                    "longitude": "111.1669420",
                    "name": "new loc 1"
                }
        """
        location = Location.objects.filter(id=existing_id).first()
        if not location:
            raise ValidationError(f"location: {existing_id} is invalid!")
        return location.__dict__

    def to_internal_value(self, data):
        # not all doctor will be created with new location
        # we need to accept existing_id also
        existing_id = data.get("id")
        if existing_id:
            data = self._get_data_from_id(existing_id)
        return super().to_internal_value(data)

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

        # location
        location_id = location_data.get("id")
        if not location_id:
            location_serializer = LocationSerializer(data=location_data)
            if location_serializer.is_valid(raise_exception=True):
                location_instance = location_serializer.save()
                location_id = location_instance.id

        # doctor
        doctor_data["location_id"] = location_id
        doctor_instance = super().create(doctor_data)

        # doctor_translation
        doctor_translation_serializer = DoctorTranslationSerializer(data=doctor_translations_data, many=True)
        if doctor_translation_serializer.is_valid(raise_exception=True):
            doctor_translation_instances = [DoctorTranslation(**doctor_translation_instance, doctor_id=doctor_instance.id) for doctor_translation_instance in doctor_translation_serializer.validated_data]
            DoctorTranslation.objects.bulk_create(doctor_translation_instances, batch_size=100)
        return doctor_instance
