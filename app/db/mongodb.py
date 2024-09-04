from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Any

class MongoDB:
    def __init__(self, url: str):
        self.client = AsyncIOMotorClient(url)
        self.db = None #self.client[settings.MONGODB_DB_NAME]

    async def connect(self, db_name: str):
        self.db = self.client[db_name]

    async def close(self):
        self.client.close()


    async def insert_document(self, collection: str, document: Dict[str, Any]) -> str:
        result = await self.db[collection].insert_one(document)
        return str(result.inserted_id)

    async def find_document(self, collection: str, query: Dict[str, Any]) -> Dict[str, Any]:
        return await self.db[collection].find_one(query)

    async def find_documents(self, collection: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        cursor = self.db[collection].find(query)
        return await cursor.to_list(length=None)

    async def update_document(self, collection: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        result = await self.db[collection].update_one(query, {"$set": update})
        return result.modified_count

    async def delete_document(self, collection: str, query: Dict[str, Any]) -> int:
        result = await self.db[collection].delete_one(query)
        return result.deleted_count

    async def get_new_documents(self, collection: str, last_sync_time: float) -> List[Dict[str, Any]]:
        query = {"created_at": {"$gt": last_sync_time}}
        return await self.find_documents(collection, query)