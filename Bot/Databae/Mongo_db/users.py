import pymongo
from Config import DATABASE_URL 
client = pymongo.MongoClient(DATABASE_URL)
db = client["cluster2"]

userdb = db["users"]

def is_served_user(user_id: int) -> bool:
    user = userdb.find_one({"bot_user": user_id})
    if not user:
        return False
    return True

def count_users() -> int:
    return userdb.count_documents({})

def get_served_users() -> list:
    users = userdb.find({"bot_user": {"$gt": 0}})
    if not users:
        return []
    users_list = []
    for user in users:
        user = user.get("bot_user")
        users_list.append(user)
    return users_list

def add_served_user(user_id: int):
    is_served = is_served_user(user_id)
    if is_served:
        return
    return  userdb.insert_one({"bot_user": user_id})

def remove_served_user(user_id: int):
    is_served = is_served_user(user_id)
    if is_served:
        return
    return  userdb.delete_one({"bot_user": user_id})
