from rest_framework import status
from rest_framework.test import APIClient
from miniproj.api.tests import BaseTests
from miniproj.api.patient.models import Patient


class PatientTests(BaseTests):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()

    def test_list_patient(self):
        response = self.client.get("/api/patient/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.patient_2.id)
        self.assertEquals(response.data["results"][1]["id"], self.patient_1.id)

    def test_retrieve_patient(self):
        response = self.client.get(f"/api/patient/{self.patient_1.id}/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["id"], self.patient_1.id)
        self.assertEquals(response.data["first_name"], self.patient_1.first_name)
        self.assertEquals(response.data["middle_name"], self.patient_1.middle_name)
        self.assertEquals(response.data["last_name"], self.patient_1.last_name)
        self.assertEquals(response.data["address"], self.patient_1.address)
        self.assertEquals(response.data["phone_number"], self.patient_1.phone_number)

    def test_create_patient(self):
        # Successful
        data = {
            "first_name": "Anthony",
            "middle_name": "Edward",
            "last_name": "Stark",
            "address": "Marvel Cinematic Universe",
            "phone_number": "123456789011",
        }
        response = self.client.post(f"/api/patient/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # With Errors
        data = {"first_name": "", "middle_name": ""}
        response = self.client.post(f"/api/patient/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data["first_name"][0], "This field may not be blank."
        )
        self.assertEquals(
            response.data["middle_name"][0], "This field may not be blank."
        )
        self.assertEquals(str(response.data["last_name"][0]), "This field is required.")
        self.assertEquals(str(response.data["address"][0]), "This field is required.")

        data = {
            "first_name": "First@name",
            "middle_name": "1234",
            "last_name": "Lastname 1234",
            "phone_number": "ABCD",
        }
        response = self.client.post(f"/api/patient/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data["first_name"][0], "Please use letters only.")
        self.assertEquals(response.data["middle_name"][0], "Please use letters only.")
        self.assertEquals(response.data["last_name"][0], "Please use letters only.")
        self.assertEquals(response.data["phone_number"][0], "Please use numbers only.")

    def test_delete_patient(self):
        # Successful
        response = self.client.delete(f"/api/patient/{self.patient_2.id}/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        patient_2 = Patient.objects.get(pk=self.patient_2.id)
        self.assertTrue(patient_2.is_deleted, True)

    def test_update_patient(self):
        data = {
            "first_name": "Spiderman",
            "middle_name": "Ben",
            "last_name": "Parker",
            "address": "Marvel Cinematic Universe",
            "phone_number": "09012172021",
        }
        response = self.client.put(
            f"/api/patient/{self.patient_1.id}/", data=data, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["id"], self.patient_1.id)
        patient_1 = Patient.objects.get(pk=self.patient_1.id)
        self.assertEquals(response.data["first_name"], patient_1.first_name)
        self.assertEquals(response.data["middle_name"], patient_1.middle_name)
        self.assertEquals(response.data["last_name"], patient_1.last_name)
        self.assertEquals(response.data["address"], patient_1.address)

    def test_list_patient_filters(self):
        response = self.client.get("/api/patient/?first_name=jack", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.patient_2.id)

        response = self.client.get("/api/patient/?last_name=par", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.patient_2.id)
        self.assertEquals(response.data["results"][1]["id"], self.patient_1.id)

    def test_list_patient_sort(self):
        response = self.client.get("/api/patient/?ordering=last_name", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.patient_1.id)
        self.assertEquals(response.data["results"][1]["id"], self.patient_2.id)

        response = self.client.get("/api/patient/?ordering=-last_name", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][1]["id"], self.patient_1.id)
        self.assertEquals(response.data["results"][0]["id"], self.patient_2.id)

        response = self.client.get("/api/patient/?ordering=address", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.patient_2.id)
        self.assertEquals(response.data["results"][1]["id"], self.patient_1.id)

        response = self.client.get("/api/patient/?ordering=-address", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][1]["id"], self.patient_2.id)
        self.assertEquals(response.data["results"][0]["id"], self.patient_1.id)

        response = self.client.get("/api/patient/?ordering=-id", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.patient_2.id)
        self.assertEquals(response.data["results"][1]["id"], self.patient_1.id)

    def test_list_patient_search(self):
        response = self.client.get("/api/patient/?search=pea", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.patient_2.id)
