from . import database2

from umongo import fields
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database2)


@instance.register
class BDSM(Document):
    id = fields.IntField(attribute='_id', required=True)
    result = fields.StrField(required=True)
    created_at = fields.DateTimeField(required=True)

    class Meta:
        collection_name = 'bdsm results'
