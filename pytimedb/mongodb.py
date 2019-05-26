#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pytimedb.mongodb

(C) Jean-François Baget 2019 
"""
from pytimedb.abstractdb import AbstractDB, NotFoundDBError
from pymongo import MongoClient

class MongoDB(AbstractDB):
    
    def __init__(self, client, database, collection):
        self.client = MongoClient(client)
        self.database = self.client[database]
        self.posts = self.database.posts

    def __del__(self):
        self.client.close()

    def abstract_get(self, key : str):
        result = self.posts.find_one({'_id' : key})
        if result is None:
            msg = "{} not present in database"
            raise NotFoundDBError(msg.format(key))
        else:
            return result

    def abstract_set(self, json_timevar):
        self.posts.replace_one({'_id' : json_timevar['_id']}, json_timevar, upsert = True)

    def abstract_enumerate(self):
        for document in self.database.posts.find():
            yield document

    def abstract_delete(self, key):
        result = self.posts.find_one_and_delete({'_id' : key})
        return result if result else {}

    def abstract_length(self):
        return self.posts.count_documents({})

    def abstract_delete_all(self):
        length = len(self)
        result = self.posts.delete_many({})
        return result.deleted_count == length

if __name__ == "__main__":
    from pytimedb.timevar import TimeVar
    database = MongoDB('mongodb://localhost:27017', 'pytimedb', 'timevars')
    timevar = TimeVar("y")
    database.set(timevar)
    print(database.get("y").to_json())