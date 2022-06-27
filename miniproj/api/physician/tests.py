from rest_framework import status
from rest_framework.test import APIClient
from miniproj.api.tests import BaseTests
from miniproj.api.physician.models import Physician


class PhysicianTests(BaseTests):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()

    def test_list_physician(self):
        response = self.client.get("/api/physician/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.physician_2.id)
        self.assertEquals(response.data["results"][1]["id"], self.physician_1.id)

    def test_retrieve_physician(self):
        response = self.client.get(
            f"/api/physician/{self.physician_1.id}/", follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["id"], self.physician_1.id)
        self.assertEquals(response.data["first_name"], self.physician_1.first_name)
        self.assertEquals(response.data["middle_name"], self.physician_1.middle_name)
        self.assertEquals(response.data["last_name"], self.physician_1.last_name)
        self.assertEquals(response.data["address"], self.physician_1.address)
        self.assertEquals(response.data["phone_number"], self.physician_1.phone_number)

    def test_create_physician(self):
        # Successful
        data = {
            "first_name": "Anthony",
            "middle_name": "Edward",
            "last_name": "Stark",
            "address": "Marvel Cinematic Universe",
            "phone_number": "123456789011",
        }
        response = self.client.post(f"/api/physician/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # With Errors
        data = {"first_name": "", "middle_name": ""}
        response = self.client.post(f"/api/physician/", data=data, follow=True)
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
        response = self.client.post(f"/api/physician/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data["first_name"][0], "Please use letters only.")
        self.assertEquals(response.data["middle_name"][0], "Please use letters only.")
        self.assertEquals(response.data["last_name"][0], "Please use letters only.")
        self.assertEquals(response.data["phone_number"][0], "Please use numbers only.")

    def test_delete_physician(self):
        # Successful
        response = self.client.delete(
            f"/api/physician/{self.physician_2.id}/", follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        physician_2 = Physician.objects.get(pk=self.physician_2.id)
        self.assertTrue(physician_2.is_deleted, True)

    def test_update_physician(self):
        data = {
            "first_name": "Spiderman",
            "middle_name": "Ben",
            "last_name": "Parker",
            "address": "Marvel Cinematic Universe",
            "phone_number": "09012172021",
        }
        response = self.client.put(
            f"/api/physician/{self.physician_1.id}/", data=data, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["id"], self.physician_1.id)
        physician_1 = Physician.objects.get(pk=self.physician_1.id)
        self.assertEquals(response.data["first_name"], physician_1.first_name)
        self.assertEquals(response.data["middle_name"], physician_1.middle_name)
        self.assertEquals(response.data["last_name"], physician_1.last_name)
        self.assertEquals(response.data["address"], physician_1.address)

    def test_list_physician_filters(self):
        response = self.client.get("/api/physician/?first_name=jose", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.physician_2.id)

        response = self.client.get("/api/physician/?last_name=rizal", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.physician_2.id)

    def test_list_physician_sort(self):
        response = self.client.get("/api/physician/?ordering=last_name", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.physician_1.id)
        self.assertEquals(response.data["results"][1]["id"], self.physician_2.id)

        response = self.client.get("/api/physician/?ordering=-last_name", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][1]["id"], self.physician_1.id)
        self.assertEquals(response.data["results"][0]["id"], self.physician_2.id)

        response = self.client.get("/api/physician/?ordering=address", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.physician_2.id)
        self.assertEquals(response.data["results"][1]["id"], self.physician_1.id)

        response = self.client.get("/api/physician/?ordering=-address", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][1]["id"], self.physician_2.id)
        self.assertEquals(response.data["results"][0]["id"], self.physician_1.id)

        response = self.client.get("/api/physician/?ordering=-id", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.physician_2.id)
        self.assertEquals(response.data["results"][1]["id"], self.physician_1.id)

    def test_list_physician_search(self):
        response = self.client.get("/api/physician/?search=ri", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.physician_2.id)
        self.assertEquals(response.data["results"][1]["id"], self.physician_1.id)
