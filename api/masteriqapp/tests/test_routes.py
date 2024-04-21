from django.test import TestCase, Client
import django.apps


class RouteTestCases(TestCase):
    def test_route(self):
        c = Client()

        response = c.post("/api/user/register/", {"username":"test", "password":"test"})
        print(response.status_code)
        assert response.status_code == 201

        response = c.post("/api/user/token/", {"username":"test", "password":"test"})
        token = "Token " + response.json()['token']
        headers = {"Authorization":token}

        response = c.get("/api/category/1/image/", headers=headers)
        assert response.status_code == 200

        response = c.get("/api/category/iq/", headers=headers)
        assert response.status_code == 200
        assert response.json()["1"]["category_name"] is not None
        assert response.json()["1"]["user_iq"] is not None


        response = c.get("/api/question/1/new/", headers=headers)
        assert response.status_code == 200
        assert response.json()['text'] is not None
        assert response.json()['category'] is not None

        response = c.post("/api/question/new_community/", {
            "question": "How old is Harry Potter at the beginning of the first book?",
            "options": ["11", "15", "He wasnt born"],
            "answer": "1"}, headers=headers)

        response = c.get("/api/question/options/", headers=headers)
        assert response.status_code == 200
        assert response.json()['question_id'] is not None
        assert response.json()['number_of_options'] is not None
        assert response.json()['options'] is not None
        assert len(response.json()['options']) >= 2

        response = c.get("/api/rank/1/leaderboard/", headers=headers)
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert response.json()[0]['user_id'] is not None
        assert response.json()[0]['user_name'] is not None
        assert response.json()[0]['user_iq'] is not None

        response = c.get("/api/rank/global_leaderboard/", headers=headers)
        assert response.status_code == 200
        assert len(response.json()) > 0
        assert response.json()[0]['user_id'] is not None
        assert response.json()[0]['user_name'] is not None
        assert response.json()[0]['user_iq'] is not None

        response = c.get("/api/rank/1/user/", headers=headers)
        assert response.status_code == 200
        assert response.json()['user_rank'] is not None
        assert response.json()['user_iq'] is not None

        response = c.get("/api/rank/global_user/", headers=headers)
        assert response.status_code == 200
        assert response.json()['user_rank'] is not None
        assert response.json()['user_iq'] is not None

        response = c.get("/api/category/2/user_iq/", headers=headers)
        assert response.status_code == 200
        assert response.json()['user_iq'] is not None
