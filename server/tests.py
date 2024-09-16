from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse


# Create your tests here.
class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')
        self.personas_url = reverse('persona-list')

        self.user_data = {
            'username': 'test-user',
            'password': 'test-user',
            'email': 'test-user@email.com'
        }

        return super().setUp()

    def register(self):
        res = self.client.post(
            self.register_url,
            data=self.user_data
        )
        return res.data

    def create_personas(self, quantity, token):
        for i in range(quantity):
            self.client.post(
                self.personas_url,
                headers={
                    'Authorization': f'Token {token}'
                },
                data={
                    'name': f'Persona {i + 1}',
                    'age': i + 1
                }
            )


class TesViews(TestSetUp):

    def test_user_cannot_register_without_data(self):
        response = self.client.post(self.register_url)
        self.assertEqual(
            response.status_code,
            400,
            msg='Succes!! test_user_cannot_register_without_data'
        )

    def test_user_can_register(self):
        response = self.client.post(
            self.register_url,
            data=self.user_data
        )

        self.assertEqual(
            response.status_code,
            201,
            msg='Succes!! test_user_can_register'
        )

    def test_user_cannot_access_profile_without_auth(self):
        response = self.client.post(self.profile_url)
        self.assertEqual(
            response.status_code,
            401,
            msg='Succes!! test_user_cannot_access_profile_without_auth'
        )

    def test_user_can_access_profile(self):
        user = self.register()

        response = self.client.post(
            self.profile_url,
            headers={
                'Authorization': f'Token {user["token"]}'
            }
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_user_can_list_personas(self):
        user = self.register()

        self.create_personas(9, user['token'])

        response = self.client.get(
            self.personas_url,
            headers={
                'Authorization': f'Token {user["token"]}'
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_user_cannot_list_personas_without_auth(self):
        response = self.client.get(
            self.personas_url,
        )

        self.assertEqual(
            response.status_code,
            401
        )
