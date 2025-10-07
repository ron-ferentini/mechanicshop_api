from app.extensions import ma
from app.models import Service_Ticket
from marshmallow import fields

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Ticket
        # include foreign key fields (e.g. customer_id) so they are accepted on load
        include_fk = True

class EditServiceTicketSchema(ma.Schema):
    add_mechanic_id = fields.List(fields.Integer())
    remove_mechanic_id = fields.List(fields.Integer())
    class Meta:
        fields = (
            "add_mechanic_id",
            "remove_mechanic_id",
        )   

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
return_loans_schema = ServiceTicketSchema(many=True)
edit_service_ticket_schema = EditServiceTicketSchema()