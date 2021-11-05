from . import database4

from umongo.fields import *
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database4)


@instance.register
class Starboard(Document):
    id = IntField(attribute='_id', required=True)
    author_id = IntField(required=True)
    starrer_id = IntField(required=True)
    starrers = ListField(IntField())
    channel_id = IntField(required=True)
    star_message_id = IntField(required=True)
    stars_count = IntField(required=True)

    class Meta:
        collection_name = 'Starboard'


@instance.register
class StarboardStats(Document):
    id = IntField(attribute='_id', required=True)
    messages_starred = IntField(required=True)
    stars_received = IntField(required=True)
    stars_given = IntField(required=True)

    class Meta:
        collection_name = 'StarboardStats'


@instance.register
class StarboardStatus(Document):
    id = IntField(attribute='_id', default='1')
    locked = BoolField(required=True)

    class Meta:
        collection_name = 'StarboardStatus'
