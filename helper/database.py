from pymongo import MongoClient
from config import Config
from .utils import send_log
import datetime
import time

myclient = MongoClient(Config.DB_URL)
mydb = myclient[Config.DB_NAME]
usrcol = mydb['users']
premium = mydb['premium_users']

class Database:

    def new_user(self, id):
        return dict(
            _id=int(id),                                   
            file_id=None,
            caption=None
        )

    async def add_user(b, m):
        u = m.from_user
        if not await is_user_exist(u.id):
            user = new_user(u.id)
            usrcol.insert_one(user)            
            await send_log(b, u)

    async def is_user_exist(id):
        user = usrcol.find_one({'_id': int(id)})
        return bool(user)

    async def total_users_count():
        count = usrcol.count_documents({})
        return count

    async def get_all_users():
        all_users = usrcol.find({})
        return all_users

    async def delete_user(user_id):
        usrcol.delete_many({'_id': int(user_id)})
    
    async def set_thumbnail(id, file_id):
        usrcol.update_one({'_id': int(id)}, {'$set': {'file_id': file_id}})

    async def get_thumbnail(id):
        user = usrcol.find_one({'_id': int(id)})
        return user.get('file_id', None)

    async def get_user(user_id):
        user_data = premium.find_one({"id": user_id})
        return user_data

    async def update_user(user_data):
        premium.update_one({"id": user_data["id"]}, {"$set": user_data}, upsert=True)

    async def has_premium_access(user_id):
        user_data = await get_user(user_id)
        if user_data:
            expiry_time = user_data.get("expiry_time")
            if expiry_time is None:
                return False
            elif isinstance(expiry_time, datetime.datetime) and datetime.datetime.now() <= expiry_time:
                return True
            else:
                premium.update_one({"id": user_id}, {"$set": {"expiry_time": None}})
        return False
    
    async def update_user(user_data):
        await premium.update_one({"id": user_data["id"]}, {"$set": user_data}, upsert=True)

    async def update_one(filter_query, update_data):
        try:
            result = premium.update_one(filter_query, update_data)
            return result.matched_count == 1
        except Exception as e:
            print(f"Error updating document: {e}")
            return False

    async def get_expired(current_time):
        expired_users = []
        if data := premium.find({"expiry_time": {"$lt": current_time}}):
            async for user in data:
                expired_users.append(user)
        return expired_users

    async def remove_premium_access(user_id):
        return await premium.update_one(
            {"id": user_id}, {"$set": {"expiry_time": None}}
            )

db = Database()




