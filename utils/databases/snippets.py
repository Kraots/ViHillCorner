from . import database1

from umongo.fields import *
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database1)


@instance.register
class Snippet(Document):
    name = IntField(attribute='_id', required=True)
    content = StrField(required=True)
    owner_id = IntField(required=True)
    uses_count = IntField(required=True)
    created_at = StrField(required=True)

    class Meta:
        collection_name = 'Snippets'
