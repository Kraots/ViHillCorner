from . import database1

from umongo.fields import *
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database1)


@instance.register
class Marriage(Document):
    id = IntField(attribute='_id', required=True)
    married_to = IntField(required=True)
    marry_date = DateTimeField(required=True)

    class Meta:
        collection_name = 'Marry Data'
