import json
from collections import Counter
from copy import deepcopy

from rest_framework import status

from hybeta.services.utils import Utils
from tests import BasePyTest


class TestDoctor(BasePyTest):
    BULK_CREATE_DOCTOR_URL = "/doctor/bulk_create/"
    DOCTOR_URL = "/doctor/"
    SINGLE_DOCTOR_PAYLOAD = {
        "doctor_translations": [{"language_code": "EN", "name": "new name 1", "note": "new note 1"}, {"language_code": "HK", "name": "new name HK 1", "note": "new note HK 1"}],
        "location": {"district": "TP", "latitude": "874.1669429", "longitude": "111.1669420", "name": "new loc 1"},
        "phone": "0905360911",
        "category": "D",
        "price": "123.11",
        "available_time": "available 1",
    }
    MULTIPLE_DOCTORS_PAYLOAD = [
        {
            "doctor_translations": [{"language_code": "EN", "name": "new name 1", "note": "new note 1"}, {"language_code": "HK", "name": "new name HK 1", "note": "new note HK 1"}],
            "location": {"district": "TP", "latitude": "874.1669429", "longitude": "111.1669420", "name": "new loc 1"},
            "phone": "0905360911",
            "category": "D",
            "price": "123.11",
            "available_time": "available 1",
        },
        {
            "doctor_translations": [{"language_code": "EN", "name": "new name 2", "note": "new note 2"}],
            "location": {"id": 2, "district": "WTS", "latitude": "112.9429000", "longitude": "112.1942900", "name": "new loc 2"},
            "phone": "20244432322",
            "category": "K",
            "price": "32432.22",
            "available_time": "available 2",
        },
    ]

    def _validate_bulk_create_doctor_response(self, response):
        response_json = response.json()
        assert response_json
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response_json, list)
        assert len(self.MULTIPLE_DOCTORS_PAYLOAD) == len(response_json)
        payload_phones = [doctor.get("phone") for doctor in self.MULTIPLE_DOCTORS_PAYLOAD]
        response_phones = [doctor.get("phone") for doctor in response_json]
        assert Counter(payload_phones) == Counter(response_phones)
        # TODO assert self.MULTIPLE_DOCTORS_PAYLOAD == remove_ids(response_json)

    def _validate_single_create_doctor_response(self, response):
        response_json = response.json()
        assert response_json
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response_json, dict)
        assert self.SINGLE_DOCTOR_PAYLOAD["phone"] == response_json["phone"]

    def test_single_create_success(self):
        response = self.client.post(self.DOCTOR_URL, json.dumps(self.SINGLE_DOCTOR_PAYLOAD), content_type="application/json")
        self._validate_single_create_doctor_response(response)
        return response.json()

    def test_bulk_create_success(self):
        response = self.client.post(self.BULK_CREATE_DOCTOR_URL, json.dumps(self.MULTIPLE_DOCTORS_PAYLOAD), content_type="application/json")
        self._validate_bulk_create_doctor_response(response)
        return response.json()

    #  thank this Unittest, just discover the bug!
    def test_bulk_create_fail_on_doctor_translations(self):
        multiple_doctors_payload = deepcopy(self.MULTIPLE_DOCTORS_PAYLOAD)
        multiple_doctors_payload[0]["doctor_translations"] = []
        response = self.client.post(self.BULK_CREATE_DOCTOR_URL, json.dumps(multiple_doctors_payload), content_type="application/json")
        response_json = response.json()
        assert response_json
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_json["message"] == "[{'non_field_errors': [ErrorDetail(string='doctor_translations: [] is invalid!', code='invalid')]}, {}]"

    def test_bulk_create_fail_on_location(self):
        multiple_doctors_payload = deepcopy(self.MULTIPLE_DOCTORS_PAYLOAD)
        multiple_doctors_payload[1]["location"] = {}
        response = self.client.post(self.BULK_CREATE_DOCTOR_URL, json.dumps(multiple_doctors_payload), content_type="application/json")
        response_json = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_json["message"] == "[{}, {'location': {'district': [ErrorDetail(string='This field is required.', code='required')]}}]"

    # TODO assert self.BULK_CREATE_PAYLOAD == remove_ids(response_json)
    def test_bulk_create_fail_on_location_latitude(self):
        multiple_doctors_payload = deepcopy(self.MULTIPLE_DOCTORS_PAYLOAD)
        multiple_doctors_payload[1]["location"]["latitude"] = 123456789.123456789
        response = self.client.post(self.BULK_CREATE_DOCTOR_URL, json.dumps(multiple_doctors_payload), content_type="application/json")
        response_json = response.json()
        assert response_json
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_json["message"] == "[{}, {'location': {'latitude': [ErrorDetail(string='Ensure that there are no more than 10 digits in total.', code='max_digits')]}}]"

    def test_get_all_doctor(self):
        bulk_create_response = self.test_bulk_create_success()
        response = self.client.get(self.DOCTOR_URL)
        response_json = response.json()
        assert Utils.compare_list(bulk_create_response, response_json)

    def test_get_doctor_with_2_filter(self):
        language_code = "EN"
        district = "WTS"
        self.test_bulk_create_success()
        response = self.client.get(self.DOCTOR_URL + f"?filter_1__language_code={language_code}&filter_4__district={district}")
        response_json = response.json()
        assert all([doctor["location"]["district"] == district for doctor in response_json])
        assert all([doctor["doctor_translations"][0]["language_code"] == language_code for doctor in response_json])

    def test_get_doctor_with_4_filter(self):
        language_code = "EN"
        price = "32432.22"
        category = "K"
        district = "WTS"
        self.test_bulk_create_success()
        response = self.client.get(self.DOCTOR_URL + f"?filter_1__language_code={language_code}&filter_2__price__gte={price}&filter_3__category={category}&filter_4__district={district}")
        response_json = response.json()
        assert all([doctor["location"]["district"] == district for doctor in response_json])
        assert all([doctor["doctor_translations"][0]["language_code"] == language_code for doctor in response_json])
        assert all([doctor["category"] == category for doctor in response_json])

    def test_get_doctor_by_id(self):
        single_create_response = self.test_single_create_success()
        response = self.client.get(self.DOCTOR_URL + "1/")
        response_json = response.json()
        assert single_create_response == response_json
