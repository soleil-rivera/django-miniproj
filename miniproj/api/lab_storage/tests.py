from rest_framework import status
from rest_framework.test import APIClient
from miniproj.api.tests import BaseTests
from miniproj.api.lab_storage.models import LabStorage


class LabStorageTests(BaseTests):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()

    def test_list_lab_storage(self):
        response = self.client.get("/api/labstorage/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_lab_storage(self):
        response = self.client.get(
            f"/api/labstorage/{self.lab_storage_1.id}/", follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["id"], self.lab_storage_1.id)
        self.assertEquals(response.data["orders"], [self.order_1.id, self.order_2.id])

    def test_create_lab_storage(self):
        data = {"name": "Lab-03", "location": "Location 3"}
        response = self.client.post(f"/api/labstorage/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {"name": "Lab US", "location": "Manila Address"}
        response = self.client.post(f"/api/labstorage/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data["detail"], "Laboratory Storage name already exists."
        )

        data = {"name": ""}
        response = self.client.post(f"/api/labstorage/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data["name"][0], "This field may not be blank.")
        self.assertEquals(str(response.data["location"][0]), "This field is required.")

        data = {"name": "Lab+01", "location": "Manila Address"}
        response = self.client.post(f"/api/labstorage/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data["name"][0],
            "Only letters, numbers, periods, hyphens and commas are allowed.",
        )

    def test_delete_lab_storage(self):
        # Successful
        response = self.client.delete(
            f"/api/labstorage/{self.lab_storage_2.id}/", follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        ls_2 = LabStorage.objects.get(pk=self.lab_storage_2.id)
        self.assertTrue(ls_2.is_deleted, True)

        # With Errors
        response = self.client.delete(
            f"/api/labstorage/{self.lab_storage_1.id}/", follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data["detail"],
            "Cannot delete LabStorage. At least 1 Order is stored.",
        )

    def test_update_lab_storage(self):
        data = {"name": "Lab-01", "location": "Location ONE"}
        response = self.client.put(
            f"/api/labstorage/{self.lab_storage_1.id}/", data=data, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["id"], self.lab_storage_1.id)
        lab_1 = LabStorage.objects.get(pk=self.lab_storage_1.id)
        self.assertEquals(response.data["name"], lab_1.name)
        self.assertEquals(response.data["location"], lab_1.location)

    def test_add_order_lab_storage(self):
        # Successful
        response = self.client.get(
            "/api/labstorage/{0}/add_order/?order_ids={1}%2C%20{2}".format(
                self.lab_storage_2.id, self.order_3.id, self.order_4.id
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # With Errors
        response = self.client.get(
            "/api/labstorage/{0}/add_order/?order_ids={1}%2C%20{2}".format(
                self.lab_storage_1.id, self.order_1.id, self.order_4.id
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data["detail"],
            "Cannot add. Order(s) {0}, {1} already stored.".format(
                self.order_1.internal_id, self.order_4.internal_id
            ),
        )

        response = self.client.get(
            "/api/labstorage/{0}/add_order/?order_ids={1}%2C%20{2}".format(
                self.lab_storage_1.id, 99, self.order_3.id
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(
            response.data["detail"],
            "Cannot add. At least one order not existing.",
        )

        response = self.client.get(
            "/api/labstorage/{}/add_order/".format(self.lab_storage_1.id),
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data["detail"],
            "No IDs provided.",
        )

        response = self.client.get(
            "/api/labstorage/{0}/add_order/?order_ids={1}%2C".format(
                self.lab_storage_1.id, self.order_3.id
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data["detail"],
            "Invalid value.",
        )

    def test_remove_order_lab_storage(self):
        # Successful
        response = self.client.get(
            "/api/labstorage/{0}/remove_order/?order_ids={1}%2C%20{2}".format(
                self.lab_storage_1.id, self.order_1.id, self.order_2.id
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # With Errors
        response = self.client.get(
            "/api/labstorage/{0}/remove_order/?order_ids={1}%2C%20{2}".format(
                self.lab_storage_1.id, self.order_3.id, self.order_4.id
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data["detail"],
            "Cannot remove. Order(s) {0}, {1} not stored in this LabStorage.".format(
                self.order_3.internal_id, self.order_4.internal_id
            ),
        )

        response = self.client.get(
            "/api/labstorage/{0}/remove_order/?order_ids={1}%2C%20{2}".format(
                self.lab_storage_1.id, 99, self.order_1.id
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(
            response.data["detail"],
            "Cannot remove. At least one order not existing.",
        )

        response = self.client.get(
            "/api/labstorage/{}/remove_order/".format(self.lab_storage_1.id),
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data["detail"],
            "No IDs provided.",
        )

        response = self.client.get(
            "/api/labstorage/{0}/remove_order/?order_ids={1}%2C".format(
                self.lab_storage_1.id, self.order_3.id
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data["detail"],
            "Invalid value.",
        )

    def test_list_labstorage_filters(self):
        response = self.client.get("/api/labstorage/?name=Laboratory", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.lab_storage_2.id)

        response = self.client.get("/api/labstorage/?location=usa", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.lab_storage_1.id)

    def test_list_labstorage_sort(self):
        response = self.client.get("/api/labstorage/?ordering=location", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.lab_storage_3.id)
        self.assertEquals(response.data["results"][1]["id"], self.lab_storage_2.id)

        response = self.client.get("/api/labstorage/?ordering=id", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.lab_storage_1.id)
        self.assertEquals(response.data["results"][1]["id"], self.lab_storage_2.id)

        response = self.client.get("/api/labstorage/?ordering=-location", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.lab_storage_1.id)
        self.assertEquals(response.data["results"][1]["id"], self.lab_storage_2.id)

        response = self.client.get("/api/labstorage/?ordering=-id", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.lab_storage_3.id)
        self.assertEquals(response.data["results"][1]["id"], self.lab_storage_2.id)

    def test_list_labstorage_search(self):
        response = self.client.get("/api/labstorage/?search=ma", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.lab_storage_3.id)
        self.assertEquals(response.data["results"][1]["id"], self.lab_storage_2.id)
