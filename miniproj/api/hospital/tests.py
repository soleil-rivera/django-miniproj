from rest_framework import status
from rest_framework.test import APIClient
from miniproj.api.tests import BaseTests
from miniproj.api.hospital.models import Hospital


class HospitalTests(BaseTests):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()

    def test_list_hospital(self):
        response = self.client.get("/api/hospital/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.hospital_1.id)
        self.assertEquals(response.data["results"][1]["id"], self.hospital_2.id)
        self.assertEquals(response.data["results"][2]["id"], self.hospital_3.id)

    def test_retrieve_hospital(self):
        response = self.client.get(f"/api/hospital/{self.hospital_1.id}/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["id"], self.hospital_1.id)
        self.assertEquals(response.data["name"], self.hospital_1.name)
        self.assertEquals(response.data["address"], self.hospital_1.address)

    def test_create_hospital(self):
        # Successful
        data = {"name": "Unciano General Hospital", "address": "Manila Address"}
        response = self.client.post(f"/api/hospital/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # With Errors
        data = {"name": "Manila Doctors Hospital", "address": "Manila Address"}
        response = self.client.post(f"/api/hospital/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data["detail"], "Hospital already exists.")

        data = {"name": ""}
        response = self.client.post(f"/api/hospital/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data["name"][0], "This field may not be blank.")
        self.assertEquals(str(response.data["address"][0]), "This field is required.")

        data = {"name": "Manila Doctors Hospital 1", "address": "Manila Address"}
        response = self.client.post(f"/api/hospital/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data["name"][0], "Please use letters only.")

    def test_delete_hospital(self):
        # Successful
        response = self.client.delete(
            f"/api/hospital/{self.hospital_2.id}/", follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        hosiptal_2 = Hospital.objects.get(pk=self.hospital_2.id)
        self.assertTrue(hosiptal_2.is_deleted, True)

    def test_update_hospital(self):
        data = {"name": "Hospital One", "address": "One Address"}
        response = self.client.put(
            f"/api/hospital/{self.hospital_1.id}/", data=data, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["id"], self.hospital_1.id)
        hospital_1 = Hospital.objects.get(pk=self.hospital_1.id)
        self.assertEquals(response.data["name"], hospital_1.name)
        self.assertEquals(response.data["address"], hospital_1.address)

    def test_list_hospital_filters(self):
        response = self.client.get("/api/hospital/?name=hospital", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.hospital_1.id)
        self.assertEquals(response.data["results"][1]["id"], self.hospital_2.id)

        response = self.client.get("/api/hospital/?address=city", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.hospital_2.id)
        self.assertEquals(response.data["results"][1]["id"], self.hospital_3.id)

    def test_list_hospital_sort(self):
        response = self.client.get("/api/hospital/?ordering=address", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.hospital_2.id)
        self.assertEquals(response.data["results"][1]["id"], self.hospital_3.id)

        response = self.client.get("/api/hospital/?ordering=-address", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.hospital_1.id)
        self.assertEquals(response.data["results"][1]["id"], self.hospital_3.id)

        response = self.client.get("/api/hospital/?ordering=-id", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.hospital_3.id)
        self.assertEquals(response.data["results"][1]["id"], self.hospital_2.id)

    def test_list_hospital_search(self):
        response = self.client.get("/api/hospital/?search=manila", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.hospital_1.id)
        self.assertEquals(response.data["results"][1]["id"], self.hospital_3.id)
