import unittest
from app import create_app


class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_index(self):
        response = self.client.get('/main_v1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to the API', response.json['messages'])


if __name__ == '__main__':
    unittest.main()
