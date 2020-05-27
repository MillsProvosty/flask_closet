from unittest import TestCase
from models import User
import json


class TestUser(TestCase):
    def test_user_has_attributes(self):
        user1 = User("Susan", "susan@email.com", "password")
        assert user1.username, "Susan"
        assert user1.password, "password"
        assert user1.email, "susan@email.com"

    def test_get_one_user(self):
        response = self.get('http://localhost:5000/users/14')
        data = json.loads(response.get_data())

        self.assertEqual(data['email'], 'gregory@example.com')
        self.assertEqual(data['first_name'], 'Gregory')
        self.assertEqual(data['last_name'], 'Anderson')
        self.assertEqual(data['phone_number'], 1234567890)
        self.assertIsNotNone(data['password'])
        self.assertEqual(data['role'], 'volunteer')