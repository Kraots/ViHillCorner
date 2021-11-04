from . import database1

from umongo import fields
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database1)


@instance.register
class Birthday(Document):
    id = fields.IntField(attribute='_id', required=True)
    birthday_date = fields.DateTimeField(required=True)
    region = fields.StrField(required=True)
    region_birthday = fields.DateTimeField(required=True)

    class Meta:
        collection_name = 'Birthdays'
