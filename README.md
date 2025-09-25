# Mechanic Shop API

A simple Flask REST API for managing customers, mechanics, and service tickets for a mechanic shop.

## Table of Contents
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Available Endpoints](#available-endpoints)
  - [Customers](#customers)
  - [Mechanics](#mechanics)
  - [Service Tickets](#service-tickets)
- [Models / Schemas](#models--schemas)
- [Examples](#examples)
- [Notes & Edge Cases](#notes--edge-cases)

## Quick Start
1. Create and activate a Python environment (Windows PowerShell example):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Ensure MySQL is running and configured. The default development database URI is defined in `config.py`:

```
mysql+mysqlconnector://root:Yankee%40143@localhost/mechanic_shop
```

Adjust credentials or use a different DB engine as needed.

3. Run the app:

```powershell
python app.py
```

The app will create tables on startup and run the Flask development server (Default: http://127.0.0.1:5000).

## Configuration
- `config.py` contains environment classes. `DevelopmentConfig` is used by default in `app.py`.
- Edit `SQLALCHEMY_DATABASE_URI` in `config.py` for your database credentials.

## Available Endpoints
Base URL: `http://127.0.0.1:5000` (when running locally)

Customers
- POST `/customers` — create a new customer
- GET `/customers` — list all customers
- GET `/customers/<id>` — retrieve a customer by id
- PUT `/customers/<id>` — update a customer (full replacement; validation enforced)
- DELETE `/customers/<id>` — delete a customer if the customer does not have a service ticket

Mechanics
- POST `/mechanics` — create a new mechanic
- GET `/mechanics` — list all mechanics
- GET `/mechanics/<id>` — retrieve a mechanic by id
- PUT `/mechanics/<id>` — update a mechanic (partial updates allowed)
- DELETE `/mechanics/<id>` — delete a mechanic

Service Tickets
- POST `/service_tickets` — create a new service ticket (must include `customer_id` that exists)
- GET `/service_tickets` — list all service tickets
- GET `/service_tickets/<id>` — retrieve a service ticket by id
- PUT `/service_tickets/<ticket_id>/assign-mechanic/<mechanic_id>` — assign a mechanic to a ticket
- DELETE `/service_tickets/<ticket_id>/remove-mechanic/<mechanic_id>` — remove a mechanic from a ticket

## Models / Schemas
The API uses SQLAlchemy models and Marshmallow schemas. Key fields:

Customer
- `id` (int)
- `name` (string, required)
- `email` (string, required)
- `phone` (string, required)

Mechanic
- `id` (int)
- `name` (string, required)
- `email` (string, required)
- `phone` (string, required)
- `salary` (float, required)

Service_Ticket
- `id` (int)
- `VIN` (string, 17 chars, required)
- `service_date` (date, required)
- `service_description` (string, required)
- `status` (string, required)
- `customer_id` (int, foreign key to `customers.id`, required)
- `mechanics` (list of assigned mechanics)

Schemas are automatically derived from models using `marshmallow-sqlalchemy`.

## Examples
Create a customer (POST /customers):

```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "555-1234"
}
```

Create a mechanic (POST /mechanics):

```json
{
  "name": "Bob Smith",
  "email": "bob@example.com",
  "phone": "555-5678",
  "salary": 45000
}
```

Create a service ticket (POST /service_tickets):

```json
{
  "VIN": "1HGCM82633A004352",
  "service_date": "2025-09-22",
  "service_description": "Oil change and inspection",
  "status": "open",
  "customer_id": 1
}
```

Assign mechanic to ticket (PUT):

PUT `/service_tickets/1/assign-mechanic/2`

Remove mechanic from ticket (DELETE):

DELETE `/service_tickets/1/remove-mechanic/2`

## Notes & Edge Cases
- Validation errors return 400 with Marshmallow error messages.
- Not-found resources return 404 with an error message.
- Assigning the same mechanic twice to a ticket returns 400.
- Removing a mechanic not assigned to the ticket returns 400.
- The app auto-creates database tables on start via `db.create_all()` in `app.py`.

## Next Steps / Improvements
- Add authentication/authorization (JWT or session-based).
- Add pagination for list endpoints.
- Add filtering/search for tickets (by status, date, VIN).
- Add unit tests and CI workflow.

If you want, I can also add example `curl` commands, Postman collection, or update `config.py` to read from environment variables.
