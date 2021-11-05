from . import database2

from umongo.fields import *
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database2)


@instance.register
class Level(Document):
    id = IntField(attribute='_id', required=True)
    xp = IntField(required=True)
    messages_count = IntField(required=True)
    weekly_messages_count = IntField(required=True)

    weekly_reset = DateTimeField()
    xp_multiplier = IntField(attribute='xp multiplier')
    booster_xp_multiplier = IntField(attribute='booster xp multiplier')
    mod_xp_multiplier = IntField(attribute='mod xp multiplier')
    kraots_xp_multiplier = IntField(attribute='kraots xp multiplier')

    class Meta:
        collection_name = 'Levels'
