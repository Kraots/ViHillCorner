from . import database1

from umongo.fields import *
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database1)


@instance.register
class Tag(Document):
    id = IntField(attribute='_id', required=True)
    name = StrField(required=True)
    content = StrField(required=True)
    owner_id = IntField(required=True)
    uses_count = IntField(required=True)
    aliases = ListField(StrField())
    created_at = StrField(required=True)

    class Meta:
        collection_name = 'Tags'
