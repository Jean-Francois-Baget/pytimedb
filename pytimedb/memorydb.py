#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pytimedb.memorydb

(C) Jean-François Baget 2019 
"""
from pytimedb.abstractdb import AbstractDB, NotFoundDBError

class MemoryDB(AbstractDB):
    
    def __init__(self):
        self.timevars = {}
    
    def abstract_get(self, key : str):
        try:
            return self.timevars[key]
        except KeyError:
            msg = "{} not present in database"
            raise NotFoundDBError(msg.format(key))

    def abstract_set(self, json_timevar):
        key = json_timevar['_id']
        self.timevars[key] = json_timevar

    def abstract_enumerate(self):
        for key in self.timevars:
            yield self.timevars[key]

    def abstract_delete(self, key):
        return self.timevars.pop(key, {})

    def abstract_length(self):
        return len(self.timevars)

    def abstract_delete_all(self):
        self.timevars = {}
        return True

if __name__ == "__main__":
    from pytimedb.timevar import TimeVar
    database = MemoryDB()
    timevar = TimeVar("x")
    database.set(timevar)
    print(database.get("x").to_json())

