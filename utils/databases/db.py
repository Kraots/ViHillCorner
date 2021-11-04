import os
import motor.motor_asyncio


key1 = os.getenv('MONGODBKEY')
cluster1 = motor.motor_asyncio.AsyncIOMotorClient(key1)
database1 = cluster1['ViHillCornerDB']

key2 = os.getenv('MONGODBLVLKEY')
cluster2 = motor.motor_asyncio.AsyncIOMotorClient(key2)
database2 = cluster2['ViHillCornerDB']

key3 = os.getenv('EXTRA_DB_KEY')
cluster3 = motor.motor_asyncio.AsyncIOMotorClient(key3)
database3 = cluster3['ViHillCornerDB']

key4 = os.getenv('MONGODBKEY2')
cluster4 = motor.motor_asyncio.AsyncIOMotorClient(key4)
database4 = cluster4['ViHillCornerDB']
