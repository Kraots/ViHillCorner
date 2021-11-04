from . import database1

from umongo import fields
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database1)


@instance.register
class Snippet(Document):
    name = fields.IntField(attribute='_id', required=True)
    content = fields.StrField(required=True)
    owner_id = fields.IntField(required=True)
    uses_count = fields.IntField(required=True)
    created_at = fields.StrField(required=True)

    class Meta:
        collection_name = 'Tags'
