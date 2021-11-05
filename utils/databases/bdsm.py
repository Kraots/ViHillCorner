from . import database2

from umongo.fields import *
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database2)


@instance.register
class BDSM(Document):
    id = IntField(attribute='_id', required=True)
    result = StrField(required=True)
    created_at = DateTimeField(required=True)

    class Meta:
        collection_name = 'bdsm results'
