#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pytimedb.insertion

(C) Jean-François Baget 2019 
"""
from pytimedb.transaction import Transaction
from pytimedb.timevar import UnsatisfiabilityError

class Insertion(Transaction):

    def can_insert(self, insertions):
        result = True
        number = 0
        while result and number < len(insertions):
            term1, term2 = insertions[number]
            result = self.insert(term1, term2)
            number += 1
        return result

    def insert(self, term1, term2):
        var1, min1, max1 = self.get_var_min_max(term1)
        var2, min2, max2 = self.get_var_min_max(term2)
        if max1 < min2:
            return True
        elif max2 < min1:
            return False
        elif term1 is int and term2 is int:
            return False
        elif type(term2) is int:
            try:
                var1.set_max(term2, self)
                return True
            except UnsatisfiabilityError:
                return False
        elif type(term1) is int:
            try:
                var2.set_min(term1, self)
                return True
            except UnsatisfiabilityError:
                return False
        else:
            upps = var1.explore_bounds('upp', self, self.get_unique(), lambda x: x.min > var1.max)
            for var in upps:
                if var.id == var2.id:
                    return True
            lows = var2.explore_bounds('low', self, self.get_unique(), lambda x: x.max > var2.min)
            for var in lows:
                if var.id == var1.id:
                    return False
            var2.low.add(var1.id)
            var1.upp.add(var2.id)
            if var2.max < var1.max:
                var1.set_max(var2.max, self)
            if var2.min > var1.min:
                var2.set_min(var1.min, self)
            return True



    def get_var_min_max(self, term):
        if type(term) is int:
            return None, term, term
        else:
            var = self.get(term, create_mode = True)
            return var, var.min, var.max

class InsertionError(ValueError):
    pass


if __name__ == '__main__':
    import random
    import time
    from pytimedb.memorydb import MemoryDB

    size_universe = 10000
    size_inserts = 100000
    delta = 3000

    universe = ["x_" + str(i) for i in range(size_universe)]
    inserts = []
    while len(inserts) < size_inserts:
        if random.random() < 0.80:
            p1 = random.randint(0, size_universe - 1)
            p2 = random.randint(0, size_universe - 1)
            if p1 < p2:
                inserts.append([universe[p1], universe[p2]])
            elif p2 < p1:
                inserts.append([universe[p2], universe[p1]])
        else:
            p = random.randint(0, size_universe - 1)
            random_delta = random.randint(0, delta) - delta//2
            truevalue = p * 100
            if random_delta >= 0:
                inserts.append([universe[p], truevalue + random_delta])
            else:
                inserts.append([truevalue + random_delta, universe[p]])

    database = MemoryDB()
    transaction = Insertion(database)

    t1 = time.time()
    result = transaction.can_insert(inserts)
    t2 = time.time()
    print(t2 - t1)

    
        

    

