from . import database2

from umongo.fields import *
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database2)


@instance.register
class ToDos(Document):
    id = IntField(attribute='_id', required=True)
    todo_data = ListField(DictField(StrField(), StrField()), required=True)

    class Meta:
        collection_name = 'Todo Data'
