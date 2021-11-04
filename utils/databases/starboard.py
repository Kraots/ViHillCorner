from . import database4

from umongo import fields
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database4)


@instance.register
class Starboard(Document):
    id = fields.IntField(attribute='_id', required=True)
    author_id = fields.IntField(required=True)
    starrer_id = fields.IntField(required=True)
    starrers = fields.ListField(fields.IntField())
    channel_id = fields.IntField(required=True)
    star_message_id = fields.IntField(required=True)
    stars_count = fields.IntField(required=True)

    class Meta:
        collection_name = 'Starboard'


@instance.register
class StarboardStats(Document):
    id = fields.IntField(attribute='_id', required=True)
    messages_starred = fields.IntField(required=True)
    stars_received = fields.IntField(required=True)
    stars_given = fields.StringField(required=True)

    class Meta:
        collection_name = 'StarboardStats'


@instance.register
class StarboardStatus(Document):
    id = fields.IntField(attribute='_id', default='1')
    locked = fields.BoolField(required=True)

    class Meta:
        collection_name = 'StarboardStatus'
