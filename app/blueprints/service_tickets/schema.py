from app.extensions import ma
from app.models import Service_Ticket

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Ticket
        # include foreign key fields (e.g. customer_id) so they are accepted on load
        include_fk = True
                    
service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)