from rest_framework.test import APITestCase
from rest_framework import status
from blog.models import Note
from django.contrib.auth.models import User

class TestNoteListCreateAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username = "serj")
        #User.objects.create_user(username="serj") #Можно и create_user()

    def test_list_objects(self):
        url = "/notes/"
        resp = self.client.get(url)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        response_data = resp.data
        expected_data = []
        self.assertEqual(expected_data, response_data)

    def test_not_empty_list_objects(self):
        Note.objects.create(title = "Test title 1", author_id = 1) #Создаем запись по id
        #Создаем физический объект класса User (получаем его из тестовой БД)
        test_user = User.objects.get(username = "serj")
        Note.objects.create(title = "Test title 2", author = test_user)

        url = "/notes/"
        resp = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, resp.status_code)

        response_data = resp.data
        self.assertEqual(2, len(response_data))

    def test_create_objects(self):
        ...

class TestNoteDetailAPIView(APITestCase):

    def test_retrieve_object(self):
        ...
