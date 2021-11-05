from . import database4

from umongo.fields import *
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database4)


@instance.register
class Ticket(Document):
    channel_id = IntField(attribute='_id', required=True)
    message_id = IntField(required=True)
    user_id = IntField(required=True)
    ticket_id = StrField(required=True)
    created_at = DateTimeField(required=True)

    class Meta:
        collection_name = 'Tickets'
