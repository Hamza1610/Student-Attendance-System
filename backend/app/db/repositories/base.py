from typing import Any, Dict, List, Optional
from pymongo.collection import Collection
from mongodb import DataBase

class Base:
    """summary: Base class for all repositories
    """
    def __init__(self, collection: Collection):
        self.db = DataBase()
        self.collection = self.db.get_collection(collection)

    async def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self.collection.find_one(query)

    async def find_all(self, query: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        cursor = self.collection.find(query)
        return await cursor.to_list(length=None)

    async def insert_one(self, document: Dict[str, Any]) -> Any:
        result = await self.collection.insert_one(document)
        return result.inserted_id

    async def update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> Any:
        result = await self.collection.update_one(query, {'$set': update})
        return result.modified_count

    async def delete_one(self, query: Dict[str, Any]) -> Any:
        result = await self.collection.delete_one(query)
        return result.deleted_count