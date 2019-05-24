#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pytimedb.timelinedb

(C) Jean-François Baget 2019 
"""
from pytimedb.timevar import TimeVar

class TimeLineDB():
    
    def __init__(self):
        self.timeline = {}

    def get(self, key : str):
        try:
            return TimeVar.from_json(self.timeline[key])
        except KeyError:
            msg = "{} not present in database"
            raise TimeLineDBError(msg.format(key))

    def set(self, timevar : TimeVar):
        self.timeline[timevar.id] = timevar.to_json()

class TimeLineDBError(LookupError):
    pass

