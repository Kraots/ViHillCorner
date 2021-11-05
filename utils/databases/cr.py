from . import database1

from umongo.fields import *
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database1)


@instance.register
class CustomRole(Document):
    id = IntField(attribute='_id', required=True)
    name = StrField(required=True)
    role_id = IntField(required=True)
    shares = IntField(required=True)
    created_at = DateTimeField(required=True)

    class Meta:
        collection_name = 'Custom Roles'
