from . import database1

from umongo.fields import *
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database1)


@instance.register
class Reminder(Document):
    id = IntField(attribute='_id', required=True)
    user_id = IntField(required=True)
    channel_id = IntField(required=True)
    message_url = StrField(required=True)
    remind_what = StrField(required=True)
    remind_when = DateTimeField(required=True)
    time_now = DateTimeField(required=True)

    class Meta:
        collection_name = 'Reminders'
