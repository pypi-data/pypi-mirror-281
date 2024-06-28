import unittest
from app import create_app


class UsersTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_get_users(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['users'], [1,2,3])


if __name__ == '__main__':
    unittest.main()
