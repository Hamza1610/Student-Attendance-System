from pymongo import MongoClient
import os
class DataBase:
    def __init__(self):
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            print('Environment variable MONGODB_URL not set')

        self.client = MongoClient(db_url)
        self.db = self.client['sas_db']

    def get_collection(self, collection_name):
        return self.db[collection_name] # database name is sas_db
    
    def get_all_collections(self):
        return self.db.list_collection_names()  
