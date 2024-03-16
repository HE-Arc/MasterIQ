from django.test import TestCase, Client
import django.apps


class RouteTestCases(TestCase):
    def test_route(self):
        c = Client()
        response = c.get("/api/category/1/image/")
        assert response.status_code == 200

        response = c.get("/api/category/iq/")
        assert response.json()["1"]["category_name"] is not None
        assert response.json()["1"]["user_iq"] is not None
        assert response.status_code == 200

        response = c.get("/api/question/1/new/")
        assert response.status_code == 200
        assert response.json()['id'] is not None
        assert response.json()['text'] is not None
        assert response.json()['category'] is not None

        response = c.post("/api/question/new_community/", {
            "question": "How old is Harry Potter at the beginning of the first book?",
            "options": ["11", "15", "He wasn\'t born"],
            "answer": "1"})
        print(response.status_code)
        assert response.status_code == 201
        assert response.json()['id'] is not None
        assert response.json()['text'] is not None
        assert response.json()['category'] is not None
        assert response.json()['options'] is not None
        assert len(response.json()['options']) >= 2
