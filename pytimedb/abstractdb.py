#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pytimedb.abstractdb

(C) Jean-François Baget 2019 
"""
from abc import ABC, abstractmethod
from pytimedb.timevar import TimeVar

class AbstractDB(ABC):

    def __len__(self):
        return self.abstract_length()

    def get(self, key: str):
        return TimeVar.from_json(self.abstract_get(key))

    def set(self, timevar : TimeVar):
        self.abstract_set(timevar.to_json())

    def enumerate(self):
        for result in self.abstract_enumerate():
            yield TimeVar.from_json(result)

    def delete(self, key : str):
        return TimeVar.from_json(self.abstract_delete(key))

    def delete_all(self):
        return self.abstract_delete_all()

    @abstractmethod
    def abstract_get(self, key : str):
        return None

    @abstractmethod
    def abstract_set(self, json_timevar):
        return False

    @abstractmethod
    def abstract_enumerate(self):
        yield None

    @abstractmethod
    def abstract_delete(self, key):
        return None

    @abstractmethod
    def abstract_length(self):
        return 0

    def abstract_delete_all(self):
        pass

class NotFoundDBError(LookupError):
    pass

    

