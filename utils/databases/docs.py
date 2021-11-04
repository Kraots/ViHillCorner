from . import database3

from umongo import fields
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database3)


@instance.register
class Doc(Document):
    package = fields.StrField(attribute='_id', required=True)
    base_url = fields.StrField(required=True)
    inventory_url = fields.StrField(required=True)

    class Meta:
        collection_name = 'Docs'


@instance.register
class DocsCache(Document):
    id = fields.StrField(attribute='_id', required=True)
    data = fields.DictField(fields.StrField(), fields.StrField())

    class Meta:
        collection_name = 'DocsCache'
