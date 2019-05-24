#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pytimedb.database.abstractdb

(C) Jean-François Baget 2019 
"""
from abc import ABCMeta

class AbstractDB(metaclass=ABCMeta):
    
    def get_transaction(self):
        pass

