from . import database3

from umongo.fields import *
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database3)


@instance.register
class Doc(Document):
    package = StrField(attribute='_id', required=True)
    base_url = StrField(required=True)
    inventory_url = StrField(required=True)

    class Meta:
        collection_name = 'Docs'


@instance.register
class DocsCache(Document):
    id = StrField(attribute='_id', required=True)
    data = DictField(StrField(), StrField())

    class Meta:
        collection_name = 'DocsCache'
