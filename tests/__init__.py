from django.test import TestCase

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db()
class BasePyTest(TestCase):
    def setUp(self):
        self.client = APIClient(**dict(HTTP_DEVICE="My Device", HTTP_APPID=1, HTTP_TYPE=8, HTTP_PUBLIC="localhost", SERVER_NAME="localhost"))
