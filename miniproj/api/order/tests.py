from rest_framework import status
from rest_framework.test import APIClient
from miniproj.api.tests import BaseTests
from miniproj.api.order.models import Order


class OrderTests(BaseTests):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()

    def test_list_order(self):
        response = self.client.get("/api/order/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.order_1.id)
        self.assertEquals(response.data["results"][1]["id"], self.order_2.id)
        self.assertEquals(response.data["results"][2]["id"], self.order_3.id)

    def test_retrieve_order(self):
        response = self.client.get(f"/api/order/{self.order_1.id}/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["id"], self.order_1.id)
        self.assertEquals(response.data["internal_id"], self.order_1.internal_id)
        self.assertEquals(
            response.data["date_sample_taken"], self.order_1.date_sample_taken
        )

    def test_create_order(self):
        # Successful
        data = {"internal_id": "Order0005", "date_sample_taken": "2022-03-11"}
        response = self.client.post(f"/api/order/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # With Errors
        data = {"internal_id": "Order0005", "date_sample_taken": "2022-03-11"}
        response = self.client.post(f"/api/order/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data["detail"], "Internal ID already exists.")

        data = {"internal_id": ""}
        response = self.client.post(f"/api/order/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data["internal_id"][0], "This field may not be blank."
        )
        self.assertEquals(
            str(response.data["date_sample_taken"][0]), "This field is required."
        )

        data = {"internal_id": "Order+0005", "date_sample_taken": "2022-03-11"}
        response = self.client.post(f"/api/order/", data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data["internal_id"][0],
            "Only letters, numbers, periods, hyphens and commas are allowed.",
        )

    def test_delete_order(self):
        # Successful
        response = self.client.delete(f"/api/order/{self.order_2.id}/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        order_2 = Order.objects.get(pk=self.order_2.id)
        self.assertTrue(order_2.is_deleted, True)

    def test_update_order(self):
        self.maxDiff = None
        data = {
            "internal_id": "Order0001",
            "date_sample_taken": "2022-03-11",
            "status": "Received",
            "sample": self.sample_3.id,
            "hospital": self.hospital_1.id,
            "physician": self.physician_2.id,
        }
        response = self.client.put(
            f"/api/order/{self.order_1.id}/", data=data, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["internal_id"], "Order0001")
        self.assertEquals(response.data["date_sample_taken"], "2022-03-11")
        self.assertEquals(response.data["physician"], self.physician_2.id)

    def test_list_order_filters(self):
        response = self.client.get("/api/order/?internal_id=4", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.order_4.id)

        response = self.client.get("/api/order/?status=stored", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.order_1.id)
        self.assertEquals(response.data["results"][1]["id"], self.order_2.id)

        response = self.client.get("/api/order/?sample=jack", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.order_2.id)
        self.assertEquals(response.data["results"][1]["id"], self.order_4.id)

        response = self.client.get("/api/order/?hospital=Providence", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.order_1.id)
        self.assertEquals(response.data["results"][1]["id"], self.order_2.id)
        self.assertEquals(response.data["results"][2]["id"], self.order_3.id)

        response = self.client.get(
            "/api/order/?sampletaken_createddt_from=2021-09-01&sampletaken_createddt_to=2021-09-29",
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.order_2.id)
        self.assertEquals(response.data["results"][1]["id"], self.order_3.id)

    def test_list_order_sort(self):
        response = self.client.get(
            "/api/order/?ordering=date_sample_taken", follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.order_1.id)
        self.assertEquals(response.data["results"][1]["id"], self.order_4.id)
        self.assertEquals(response.data["results"][2]["id"], self.order_2.id)
        self.assertEquals(response.data["results"][3]["id"], self.order_3.id)

        response = self.client.get(
            "/api/order/?ordering=-date_sample_taken", follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][3]["id"], self.order_1.id)
        self.assertEquals(response.data["results"][2]["id"], self.order_4.id)
        self.assertEquals(response.data["results"][1]["id"], self.order_2.id)
        self.assertEquals(response.data["results"][0]["id"], self.order_3.id)

        response = self.client.get("/api/order/?ordering=status", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.order_3.id)
        self.assertEquals(response.data["results"][1]["id"], self.order_4.id)
        self.assertEquals(response.data["results"][2]["id"], self.order_1.id)
        self.assertEquals(response.data["results"][3]["id"], self.order_2.id)

        response = self.client.get("/api/order/?ordering=-status", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][3]["id"], self.order_4.id)
        self.assertEquals(response.data["results"][2]["id"], self.order_3.id)
        self.assertEquals(response.data["results"][1]["id"], self.order_2.id)
        self.assertEquals(response.data["results"][0]["id"], self.order_1.id)

        response = self.client.get("/api/order/?ordering=physician", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.order_1.id)
        self.assertEquals(response.data["results"][1]["id"], self.order_2.id)

    def test_list_order_search(self):
        response = self.client.get("/api/order/?search=peter", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data["results"][0]["id"], self.order_1.id)
        self.assertEquals(response.data["results"][1]["id"], self.order_3.id)
