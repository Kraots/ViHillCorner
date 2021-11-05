from . import database1

from umongo.fields import *
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database1)


@instance.register
class Birthday(Document):
    id = IntField(attribute='_id', required=True)
    birthday_date = DateTimeField(required=True)
    region = StrField(required=True)
    region_birthday = DateTimeField(required=True)

    class Meta:
        collection_name = 'Birthdays'
