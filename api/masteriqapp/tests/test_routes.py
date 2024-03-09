from django.test import TestCase, Client
import django.apps


class RouteTestCases(TestCase):
    def test_route(self):
        c = Client()
        response = c.get("/category/1/image/")
        assert response.status_code == 200

        response = c.get("/category/iq/")
        assert response.json()["1"]["category_name"] is not None
        assert response.json()["1"]["user_iq"] is not None
        assert response.status_code == 200