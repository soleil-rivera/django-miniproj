from rest_framework.test import APITestCase, APIClient
from miniproj.constants import OrderStatus
from miniproj.api.hospital.models import Hospital
from miniproj.api.lab_storage.models import LabStorage
from miniproj.api.order.models import Order
from miniproj.api.patient.models import Patient
from miniproj.api.physician.models import Physician
from miniproj.api.sample.models import Sample


class BaseTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()

        cls.hospital_1, _ = Hospital.objects.get_or_create(
            name="Manila Doctors Hospital",
            address="S667 United Nations Ave, Ermita, Manila, 1000 Metro Manila",
        )
        cls.hospital_2, _ = Hospital.objects.get_or_create(
            name="Providence Hospital",
            address="1515 Quezon Ave, Diliman, Quezon City, 198702",
        )
        cls.hospital_3, _ = Hospital.objects.get_or_create(
            name="VRP Medical Center",
            address="163 Epifanio de los Santos Ave, Mandaluyong City, 1501 Metro Manila",
        )

        cls.patient_1, _ = Patient.objects.get_or_create(
            first_name="Peter",
            middle_name="Benjamin",
            last_name="Parker",
            address="2021 No Way Home",
            phone_number="09012172021",
        )
        cls.patient_2, _ = Patient.objects.get_or_create(
            first_name="Jack",
            middle_name="Teague",
            last_name="Sparrow",
            address="2003 Black Pearl St. Carribean ",
        )

        cls.physician_1, _ = Physician.objects.get_or_create(
            first_name="Soleil",
            middle_name="Smith",
            last_name="Rivera",
            address="213 Address St. Manila City",
            phone_number="09123456789",
        )
        cls.physician_2, _ = Physician.objects.get_or_create(
            first_name="Jose",
            middle_name="Protacio",
            last_name="Rizal",
            address="09987654321",
        )

        cls.sample_1, _ = Sample.objects.get_or_create(
            sample_id="Sample-peter-0001", first_name=cls.patient_1
        )
        cls.sample_2, _ = Sample.objects.get_or_create(
            sample_id="Sample-jack-0002", first_name=cls.patient_2
        )
        cls.sample_3, _ = Sample.objects.get_or_create(
            sample_id="Sample-jack-0003", first_name=cls.patient_2
        )

        cls.order_1, _ = Order.objects.get_or_create(
            internal_id="Order0001",
            date_sample_taken="2021-05-21",
            status=OrderStatus.RECEIVED,
            sample=cls.sample_1,
            hospital=cls.hospital_2,
            physician=cls.physician_2,
        )
        cls.order_2, _ = Order.objects.get_or_create(
            internal_id="Order0002",
            date_sample_taken="2021-09-07",
            status=OrderStatus.RECEIVED,
            sample=cls.sample_2,
            hospital=cls.hospital_2,
            physician=cls.physician_2,
        )
        cls.order_3, _ = Order.objects.get_or_create(
            internal_id="Order0003",
            date_sample_taken="2021-09-08",
            status=OrderStatus.RECEIVED,
            sample=cls.sample_1,
            hospital=cls.hospital_2,
            physician=cls.physician_2,
        )
        cls.order_4, _ = Order.objects.get_or_create(
            internal_id="Order0004",
            date_sample_taken="2021-08-19",
            status=OrderStatus.RECEIVED,
            sample=cls.sample_3,
            hospital=cls.hospital_1,
            physician=cls.physician_1,
        )

        cls.lab_storage_1, _ = LabStorage.objects.get_or_create(
            name="Lab US", location="San Francisco, USA"
        )
        cls.lab_storage_2, _ = LabStorage.objects.get_or_create(
            name="Laboratory PH", location="Manila, Philippines"
        )
        cls.lab_storage_3, _ = LabStorage.objects.get_or_create(
            name="Lab MY", location="Malaysia"
        )

        cls.lab_storage_1.orders.add(cls.order_1)
        cls.order_1.status = OrderStatus.STORED
        cls.order_1.save()
        cls.lab_storage_1.orders.add(cls.order_2)
        cls.order_2.status = OrderStatus.STORED
        cls.order_2.save()
