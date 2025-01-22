from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Post

class SchedulingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="adminpassword", is_staff=True)
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_schedule_post(self):
        data = {
            "title": "Test Post",
            "content": "Test Content",
            "status": "draft",
            "scheduled_time": "2025-01-21T10:00:00Z",
            "timezone": "UTC"
        }
        response = self.client.post("/content/schedule/", data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_bulk_schedule(self):
        with open("C:\\Users\\This  PC\\Downloads\\bulk_schedule_test.csv", "rb") as f:
            response = self.client.post("/content/schedule/bulk/", {"file": f})
        self.assertEqual(response.status_code, 201)

    def test_list_scheduled_posts(self):
        response = self.client.get("/content/schedule/calendar/")
        self.assertEqual(response.status_code, 200)
