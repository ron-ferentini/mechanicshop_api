from app import create_app
from app.models import db, Mechanic
import unittest

class TestMechanic(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.mechanic = Mechanic(name="test_mechanic", email="test@mechanic.com", phone="770-123-4567", salary=50000, password='test')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
        self.client = self.app.test_client()
        
    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "Jane Smith",
            "email": "jane@mechanic.com",
            "phone": "770-987-6543",
            "salary": 60000,
            "password": "test"
        }

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Jane Smith")
    
    def test_invalid_creation(self):
        mechanic_payload = {
            "name": "Jane Smith",
            "phone": "770-987-6543",
            "salary": 60000,
            "password": "test"
        }

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])

    def test_mechanic_login(self):
        login_payload = {
            "email": "test@mechanic.com",
            "password": "test"
        }

        response = self.client.post('/mechanics/login', json=login_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']

    def test_invalid_login(self):
        login_payload = {
            "email": "bad_email@mechanic.com",
            "password": "bad_password"
        }

        response = self.client.post('/mechanics/login', json=login_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Invalid email or password!')
        
    def test_get_mechanics(self):
        response = self.client.get('/mechanics/?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 1)
        
    def test_get_mechanic(self):
        response = self.client.get(f'/mechanics/{self.mechanic.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], 'test@mechanic.com')
        
    