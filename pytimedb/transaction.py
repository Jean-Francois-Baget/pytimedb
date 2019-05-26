#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pytimedb.transaction

(C) Jean-François Baget 2019 
"""
from pytimedb.timevar import TimeVar
from pytimedb.abstractdb import NotFoundDBError
 
class Transaction():
    
    def __init__(self, database):
        self.database = database
        self.buffer = {}
        self.unique = 0

    def get(self, key : str, create_mode = False):
        try: 
            return self.buffer[key]
        except KeyError:
            try:
                timevar = self.database.get(key)
                timevar.modified = False
            except NotFoundDBError:
                if create_mode:
                    timevar = TimeVar(key)
                    timevar.modified = True
                else:
                    msg = "{} not present in database, create mode disabled."
                    raise TransactionError(msg.format(key))
            self.buffer[key] = timevar
            return timevar

    def push(self, empty = False):
        for key in self.buffer:
            timevar = self.buffer[key]
            if timevar.modified:
                self.database.set(timevar)
                timevar.modified = False
        if empty:
            self.buffer = {}

    def get_unique(self):
        result = str(self.unique)
        self.unique += 1
        return "{}_{}".format(str(id(self)), result) 

    def ask_inf(self, term1, term2):
        var1, min1, max1 = self.get_var_min_max(term1)
        var2, min2, max2 = self.get_var_min_max(term2)
        if max1 < min2:
            return True
        elif max2 < min1: ## should clarify the algebra, but it seems this is it
            return False
        elif var1 is None or var2 is None:
            return False
        else:
            upps = var1.explore_bounds('upp', self, self.get_unique(), lambda x: x.min > var1.max)
            for var in upps:
                if var.id == var2.id:
                    return True
            return False

    def get_var_min_max(self, term):
        if type(term) is int:
            return None, term, term
        else:
            var = self.get(term, create_mode = True)
            return var, var.min, var.max

class TransactionError(LookupError):
    pass