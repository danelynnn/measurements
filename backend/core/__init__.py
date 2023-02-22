from pymongo import MongoClient

db_client = MongoClient(
    'mongodb+srv://danelynnn:s99UMbDSv5zZRzSV@cluster0.qucl8rc.mongodb.net/retryWrites=true&w=majority')
SALT = bytes('salty', 'utf-8')
SECRET_KEY = b'7[\x7f\rl\xe7\xa4\xfbc\xe2\xc1MxKg\x08\xf9w/P\x17X\xf6L'
