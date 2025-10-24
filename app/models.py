from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select
from datetime import date
from typing import List

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

service_ticket_mechanic = db.Table(
    'service_ticket_mechanic',
    Base.metadata,
    db.Column('ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'), primary_key=True)
)

class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(15), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    
    service_tickets: Mapped[List["Service_Ticket"]] = db.relationship(back_populates='customer')

class Service_Ticket(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(17), nullable=False)
    service_date: Mapped[date] = mapped_column(db.Date, nullable=False)
    service_description: Mapped[str] = mapped_column(db.String(250), nullable=False)
    status: Mapped[str] = mapped_column(db.String(50), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'), nullable=False)

    customer: Mapped['Customer'] = db.relationship(back_populates='service_tickets')
    mechanics: Mapped[List["Mechanic"]] = db.relationship(secondary=service_ticket_mechanic, back_populates='service_tickets')
    service_ticket_inventory: Mapped[List["Service_Ticket_Inventory"]] = db.relationship(back_populates='service_ticket')

class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(15), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    service_tickets: Mapped[List["Service_Ticket"]] = db.relationship(secondary=service_ticket_mechanic, back_populates='mechanics')

class Inventory(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    part_name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)

    service_ticket_inventory: Mapped[List["Service_Ticket_Inventory"]] = db.relationship(back_populates='inventory')

class Service_Ticket_Inventory(Base):
    __tablename__ = 'service_ticket_inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_id: Mapped[int] = mapped_column(db.ForeignKey('service_tickets.id'), primary_key=True)
    inventory_id: Mapped[int] = mapped_column(db.ForeignKey('inventory.id'), primary_key=True)
    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False)
    total_price: Mapped[float] = mapped_column(db.Float, nullable=False)

    service_ticket: Mapped['Service_Ticket'] = db.relationship(back_populates='service_ticket_inventory')
    inventory: Mapped['Inventory'] = db.relationship(back_populates='service_ticket_inventory')