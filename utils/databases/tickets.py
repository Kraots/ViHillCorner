from . import database4

from umongo import fields
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database4)


@instance.register
class Ticket(Document):
    channel_id = fields.IntField(attribute='_id', required=True)
    message_id = fields.IntField(required=True)
    user_id = fields.IntField(required=True)
    ticket_id = fields.StringField(required=True)
    created_at = fields.DateTimeField(required=True)

    class Meta:
        collection_name = 'Tickets'
