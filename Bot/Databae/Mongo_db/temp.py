import pymongo
from Config import DATABASE_URL 
client = pymongo.MongoClient(DATABASE_URL)
db = client["cluster2"]
temp_db = db["temp"]

async def get_temp(message_status: str):
    temps =  temp_db.find_one({f"message_status": message_status})
    if not temps:
        return False
    return temps
def add_note(message_status: str,text: str):
    data = {"text": text, "message_status": message_status}
    return temp_db.insert_one(data)

def edit_note(message_status,text):
    return temp_db.update_one({"message_status": message_status}, {"$set": {"text": text}})
