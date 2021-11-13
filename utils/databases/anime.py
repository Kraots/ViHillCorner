from . import database1

from umongo.fields import *
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database1)


@instance.register
class Alist(Document):
    id = IntField(attribute='_id', required=True)
    alist = ListField(StrField(), default=[])
    mlist = ListField(StrField(), default=[])

    class Meta:
        collection_name = 'Alist'
