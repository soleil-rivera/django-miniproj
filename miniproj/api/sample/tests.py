from rest_framework import status
from rest_framework.test import APIClient
from miniproj.api.tests import BaseTests
from miniproj.api.sample.models import Sample


class SampleTests(BaseTests):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()

    def test_list_sample(self):
        response = self.client.get("/api/sample/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.sample_2.id)
        self.assertEquals(response.data["results"][1]["id"], self.sample_3.id)
        self.assertEquals(response.data["results"][2]["id"], self.sample_1.id)

    def test_retrieve_sample(self):
        response = self.client.get(f"/api/sample/{self.sample_1.id}/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["id"], self.sample_1.id)
        self.assertEquals(response.data["sample_id"], self.sample_1.sample_id)
        self.assertEquals(response.data["first_name"], self.sample_1.first_name.id)

    def test_create_sample(self):
        # Successful
        data = {"sample_id": "Sample-peter-0004", "first_name": self.patient_1.id}
        response = self.client.post(f"/api/sample/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # With Errors
        data = {"sample_id": "Sample-peter-0004", "first_name": self.patient_1.id}
        response = self.client.post(f"/api/sample/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data["detail"], "Sample ID already exists.")

        data = {"sample_id": ""}
        response = self.client.post(f"/api/sample/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data["sample_id"][0], "This field may not be blank.")
        self.assertEquals(
            str(response.data["first_name"][0]), "This field is required."
        )

        data = {"sample_id": "s@mple", "first_name": self.patient_1.id}
        response = self.client.post(f"/api/sample/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data["sample_id"][0],
            "Only letters, numbers, periods, hyphens and commas are allowed.",
        )

    def test_delete_sample(self):
        # Successful
        response = self.client.delete(f"/api/sample/{self.sample_2.id}/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        sample_2 = Sample.objects.get(pk=self.sample_2.id)
        self.assertTrue(sample_2.is_deleted, True)

    def test_update_sample(self):
        data = {"sample_id": "Sample-peter-0005", "first_name": self.patient_1.id}
        response = self.client.put(
            f"/api/sample/{self.sample_1.id}/", data=data, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["id"], self.sample_1.id)

        sample_1 = Sample.objects.get(pk=self.sample_1.id)
        self.assertEquals(response.data["sample_id"], sample_1.sample_id)

    def test_list_sample_filters(self):
        response = self.client.get("/api/sample/?first_name=jack", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.sample_2.id)
        self.assertEquals(response.data["results"][1]["id"], self.sample_3.id)

        response = self.client.get("/api/sample/?sample_id=sample", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.sample_2.id)
        self.assertEquals(response.data["results"][1]["id"], self.sample_3.id)
        self.assertEquals(response.data["results"][2]["id"], self.sample_1.id)

    def test_list_sample_sort(self):
        response = self.client.get("/api/sample/?ordering=sample_id", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.sample_2.id)
        self.assertEquals(response.data["results"][1]["id"], self.sample_3.id)
        self.assertEquals(response.data["results"][2]["id"], self.sample_1.id)

        response = self.client.get("/api/sample/?ordering=-sample_id", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][2]["id"], self.sample_2.id)
        self.assertEquals(response.data["results"][1]["id"], self.sample_3.id)
        self.assertEquals(response.data["results"][0]["id"], self.sample_1.id)

        response = self.client.get("/api/sample/?ordering=first_name", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.sample_2.id)
        self.assertEquals(response.data["results"][1]["id"], self.sample_3.id)
        self.assertEquals(response.data["results"][2]["id"], self.sample_1.id)

        response = self.client.get("/api/sample/?ordering=-first_name", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.sample_2.id)
        self.assertEquals(response.data["results"][1]["id"], self.sample_3.id)

        response = self.client.get("/api/sample/?ordering=-id", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.sample_3.id)
        self.assertEquals(response.data["results"][1]["id"], self.sample_2.id)
        self.assertEquals(response.data["results"][2]["id"], self.sample_1.id)

    def test_list_sample_search(self):
        response = self.client.get("/api/sample/?search=pe", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.sample_1.id)
