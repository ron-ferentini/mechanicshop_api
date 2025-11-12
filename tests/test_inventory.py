from app import create_app
from app.models import db, Inventory
import unittest

class TestInventory(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.inventory_item = Inventory(name="Test Item", description="Test Description", quantity=10, price=99.99)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.inventory_item)
            db.session.commit()
        self.client = self.app.test_client()
        
    def test_create_inventory(self):
        inventory_payload = {
            "part_name": "New Item",
            "price": 49.99
        }

        response = self.client.post('/inventory/', json=inventory_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "New Item")
        
    def test_invalid_create_inventory(self):    
        inventory_payload = {
            "part_name": "New Item"
        }

        response = self.client.post('/inventory/', json=inventory_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['price'], ['Missing data for required field.'])
        
    def test_get_all_inventory_items(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        
    def test_get_single_inventory_item(self):
        response = self.client.get(f'/inventory/{self.inventory_item.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Test Item")
        
    def test_get_nonexistent_inventory_item(self):
        response = self.client.get('/inventory/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], "Inventory item not found")
        
    def test_delete_inventory_item(self):
        response = self.client.delete(f'/inventory/{self.inventory_item.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Inventory item deleted")
        
    def test_delete_nonexistent_inventory_item(self):
        response = self.client.delete('/inventory/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], "Inventory item not found")
        
    def test_update_inventory_item(self):
        response = self.client.delete(f'/inventory/{self.inventory_item.id}')
        update_payload = {
            "part_name": "Updated Item",
            "price": 79.99
        }
        response = self.client.put(f'/inventory/{self.inventory_item.id}', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Updated Item")
        
    def test_update_nonexistent_inventory_item(self):
        response = self.client.put('/inventory/999')
        update_payload = {
            "part_name": "Updated Item",
            "price": 79.99
        }

        response = self.client.put('/inventory/999', json=update_payload)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], "Inventory item not found")
    
