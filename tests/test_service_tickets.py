from app import create_app
from app.models import db, Service_Ticket
import unittest

def setUp(self):
    self.app = create_app('TestingConfig')
    self.service_ticket = Service_Ticket(description="test_service_ticket", customer_id=1)
    with self.app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(self.service_ticket)
        db.session.commit()
    self.client = self.app.test_client()
    
def test_create_service_ticket(self):
    service_ticket_payload = {
        "VIN": "1HGCM82633A004352",
        "service_date": "2024-06-01",
        "service_description": "New Service Ticket",
        "status": "Open",
        "customer_id": 1
    }
    response = self.client.post('/service_tickets', json=service_ticket_payload)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json['description'], "New Service Ticket")
    
def test_invalid_create_service_ticket(self):
    service_ticket_payload = {
        "VIN": "1HGCM82633A004352",
        "service_date": "2024-06-01",
        "status": "Open",
        "customer_id": 1
    }
    response = self.client.post('/service_tickets', json=service_ticket_payload)
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.json['service_description'], ['Missing data for required field.'])
    
def update_service_ticket(self):
    response = self.client.put(f'/service_tickets/{self.service_ticket.id}/assign-mechanic/1')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['message'], "Mechanic assigned to Service Ticket")
    
def test_invalid_update_service_ticket(self):
    response = self.client.put('/service_tickets/999/assign-mechanic/1')
    self.assertEqual(response.status_code, 404)
    self.assertEqual(response.json['error'], "Service Ticket not found")
    
def test_invalid_update_mechanic(self):
    response = self.client.put(f'/service_tickets/{self.service_ticket.id}/assign-mechanic/999')
    self.assertEqual(response.status_code, 404)
    self.assertEqual(response.json['error'], "Mechanic not found")
    
def delete_service_ticket(self):
    response = self.client.delete(f'/service_tickets/{self.service_ticket.id}/remove-mechanic/1')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['message'], "Mechanic removed from Service Ticket")
    
def get_all_service_tickets(self):
    response = self.client.get('/service_tickets')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.json), 1) 
    
def get_customer_service_tickets(self):
    response = self.client.get('/my-tickets')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.json), 1)
    self.assertEqual(response.json[0]['description'], "test_service_ticket")
    
def update_service_ticket(self):
    response = self.client.put(f'/service_tickets/{self.service_ticket.id}/assign-mechanic/1')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['message'], "Mechanic assigned to Service Ticket")
    
if __name__ == '__main__':
    unittest.main()    