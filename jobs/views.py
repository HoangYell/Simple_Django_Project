from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.decorators import action

from hybeta.services.decorators import response
from hybeta.services.utils import Utils
from jobs.models import Doctor
from jobs.serializers.doctor import DoctorCreateSerializer, DoctorSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    @staticmethod
    def get_serialized_data(params, mandatory_filter=None):
        doctor_queryset = Utils.params_2_queryset(Doctor, params, mandatory_filter=mandatory_filter)
        serializer = DoctorSerializer(doctor_queryset, many=True, context=params)
        return serializer.data

    @method_decorator(response)
    def list(self, request):
        """
        @apiVersion 1.0.0
        @api {GET} /doctor List all doctors
        @apiName ListDoctor
        @apiGroup Jobs
        @apiPermission ReadOnly
        @apiParam {Number} None
        @apiParamExample {json} Request-Example:
        http://127.0.0.1:8000/doctor?filter_1__location_id=1&sort_1__price=desc&sort_2__id=asc
        {
            "filter_1__location_id": "1",
            "sort_1__price": "desc",
            "sort_2__id": "asc",
        }
        @apiSuccessExample {json} Success-Response
        [
            {
                "id": 11,
                "doctor_translations": [
                    {
                        "id": 21,
                        "language_code": "EN",
                        "name": "new name 2",
                        "note": "new note 2"
                    }
                ],
                "location": {
                    "id": 1,
                    "district": "WTS",
                    "latitude": "112.9429000",
                    "longitude": "112.1942900",
                    "name": "new loc 2"
                },
                "phone": "20244432322",
                "category": "K",
                "price": "32432.22",
                "available_time": "available 2"
            }
        ]
        """
        data = self.get_serialized_data(request.query_params.dict().copy())
        return data

    @method_decorator(response)
    def retrieve(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {GET} /doctor/:doctor_id/language_code=:language_code retrieve by doctor_id & language
        @apiName RetrieveDoctor
        @apiGroup Jobs
        @apiPermission ReadOnly
        @apiParam {Number} None
        @apiParamExample {json} Request-Example:
        http://127.0.0.1:8000/doctor/15?filter_1__language_code=HK
        {
            "filter_1__language_code": "HK",
        }
        @apiSuccessExample {json} Success-Response
        {
            "id": 15,
            "doctor_translations": [
                {
                    "id": 23,
                    "language_code": "HK",
                    "name": "new name HK 1",
                    "note": "new note HK 1"
                }
            ],
            "location": {
                "id": 15,
                "district": "TP",
                "latitude": "111.1669429",
                "longitude": "111.1669420",
                "name": "new loc 1"
            },
            "phone": "0905360911",
            "category": "D",
            "price": "123.11",
            "available_time": "available 1"
        }
        """
        pk = kwargs.get("pk")
        data = self.get_serialized_data(request.query_params.dict().copy(), mandatory_filter=dict(pk=pk))
        return data[0] if data else {}

    @method_decorator(response)
    @action(detail=False, methods=["POST"], permission_classes=())
    def bulk_create(self, request):
        """
        @apiVersion 1.0.0
        @api {GET} /doctor/bulk_create
        @apiName BulkDoctor
        @apiGroup Jobs
        @apiPermission None
        @apiParam {Number} None
        @apiParamExample {json} Request-Example:
        http://127.0.0.1:8000/doctor/bulk_create
        [
            {
                "doctor_translations": [
                    {
                        "language_code": "EN",
                        "name": "new name 1",
                        "note": "new note 1"
                    },
                    {
                        "language_code": "HK",
                        "name": "new name HK 1",
                        "note": "new note HK 1"
                    }
                ],
                "location": {
                    "district": "TP",
                    "latitude": "111.1669429",
                    "longitude": "111.1669420",
                    "name": "new loc 1"
                },
                "phone": "0905360911",
                "category": "D",
                "price": "123.11",
                "available_time": "available 1"
            },
            {
                "doctor_translations": [
                    {
                        "language_code": "EN",
                        "name": "new name 2",
                        "note": "new note 2"
                    }
                ],
                "location": {
                    "id": 2,
                    "district": "WTS",
                    "latitude": "112.9429000",
                    "longitude": "112.1942900",
                    "name": "new loc 2"
                },
                "phone": "20244432322",
                "category": "K",
                "price": "32432.22",
                "available_time": "available 2"
            }
        ]
        @apiSuccessExample {json} Success-Response
        [
            {
                "id": 15,
                "doctor_translations": [
                    {
                        "id": 23,
                        "language_code": "HK",
                        "name": "new name HK 1",
                        "note": "new note HK 1"
                    },
                    {
                        "id": 22,
                        "language_code": "EN",
                        "name": "new name 1",
                        "note": "new note 1"
                    }
                ],
                "location": {
                    "id": 15,
                    "district": "TP",
                    "latitude": "111.1669429",
                    "longitude": "111.1669420",
                    "name": "new loc 1"
                },
                "phone": "0905360911",
                "category": "D",
                "price": "123.11",
                "available_time": "available 1"
            },
            {
                "id": 16,
                "doctor_translations": [
                    {
                        "id": 24,
                        "language_code": "EN",
                        "name": "new name 2",
                        "note": "new note 2"
                    }
                ],
                "location": {
                    "id": 16,
                    "district": "WTS",
                    "latitude": "112.9429000",
                    "longitude": "112.1942900",
                    "name": "new loc 2"
                },
                "phone": "20244432322",
                "category": "K",
                "price": "32432.22",
                "available_time": "available 2"
            }
        ]
        """
        serializer = DoctorCreateSerializer(data=request.data, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return serializer.data
