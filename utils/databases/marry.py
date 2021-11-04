from . import database1

from umongo import fields
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database1)


@instance.register
class Marriage(Document):
    id = fields.IntField(attribute='_id', required=True)
    married_to = fields.IntField(required=True)
    marry_date = fields.DateTimeField(required=True)

    class Meta:
        collection_name = 'Marry Data'
