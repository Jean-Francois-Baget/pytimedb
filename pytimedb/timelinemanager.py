from pytime.timelinedb import TimeLineDB, TimeLineDBError
from pytime.transaction import Transaction, TransactionError

class TimeLineManager():

    def __init__(self, timelinedb : TimeLineDB):
        self.timelinedb = timelinedb
        self.unique = 0

    def new_Transaction(self):
        return Transaction(self.timelinedb)

    def get(self, key : str, transaction : Transaction):
        return transaction.get(key)

    def get_unique(self):
        result = str(self.unique)
        self.unique += 1
        return "{}_{}".format(str(id(self)), result) 

    def ask_inf(self, term1, term2, transaction = False):
        if not transaction:
            transaction = Transaction(self.timelinedb)
        var1, min1, max1 = self.get_var_min_max(term1, transaction)
        var2, min2, max2 = self.get_var_min_max(term2, transaction)
        if max1 < min2:
            return True
        elif max2 < min1: ## should clarify the algebra, but it seems this is it
            return False
        elif var1 is None or var2 is None:
            return False
        else:
            upps = var1.explore_bounds('upp', transaction, self.get_unique(), lambda x: x.min > var1.max)
            for var in upps:
                if var.id == var2.id:
                    return True
            return False

    @staticmethod
    def get_var_min_max(term, transaction, create_mode = False):
        if type(term) is int:
            return None, term, term
        else:
            try:
                var = transaction.get(term, create_mode)
                min, max = var.min, var.max
                return var, min, max
            except TransactionError:
                return None, float('-inf'), float('inf')
    
    def insert_inf(self, term1, term2, transaction = False):
        if not transaction:
            transaction = Transaction(self.timelinedb)
        var1, min1, max1 = self.get_var_min_max(term1, transaction, True)
        var2, min2, max2 = self.get_var_min_max(term2, transaction, True)
        if max1 < min2:
            return True
        elif max2 < min1:
            return False
        elif term1 is int and term2 is int:
            return False
        elif type(term2) is int:
            var1.set_max(term2, transaction)
        elif type(term1) is int:
            var2.set_min(term1, transaction)
        else:
            var1.set_upp(var2)
            var2.set_low(var1)

if __name__ == "__main__":
    timelinedb = TimeLineDB()
    manager = TimeLineManager(timelinedb)
    
    insertions = [[12, 17], ["x", 150], [50, 'x'], [160, 'y']]
    questions = [["x", "y"]]

    transaction = Transaction(timelinedb)
    for elem in insertions:
        print("------------------------------------------------------------------")
        result = manager.insert_inf(elem[0], elem[1], transaction)
        print("Insertion", elem[0], "<", elem[1], ":", result)
        print("------------------------------------------------------------------")
        for key, val in transaction.timeline.items():
            print(val.to_json(), "modified:", val.modified)

    print(manager.ask_inf("x", "y", transaction))
    

