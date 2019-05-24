
class TimeVar():
    
    def __init__(self, id, min = float('-inf'), max = float('inf'), low = set([]), upp = set([])):
        self.id = id
        self.min = min
        self.max = max
        self.low = low
        self.upp = upp


    @classmethod
    def from_json(cls, json_timevar : dict):
        return cls(json_timevar['_id'], 
                   min = cls.__json_to_number(json_timevar['min']),
                   max = cls.__json_to_number(json_timevar['max']),
                   low = set(json_timevar['low']),
                   upp = set(json_timevar['upp']))

    def to_json(self):
        return {
            '_id' : self.id,
            'min' : self.__number_to_json(self.min),
            'max' : self.__number_to_json(self.max),
            'low' : list(self.low),
            'upp' : list(self.upp)
        }

    @staticmethod
    def __json_to_number(json_code):
        try:
            return int(json_code)
        except ValueError:
            return float(json_code)

    @staticmethod
    def __number_to_json(number):
        if type(number) is int:
            return number
        else:
            return str(number)

    def set_max(self, max : int, transaction):
        if max < self.max:
            if self.min > max:
                msg = "{} cannot have min {} and max {}."
                raise UnsatisfiabilityError(msg.format(self.id, self.min, self.max))
            self.max = max
            self.modified = True
            for uppname in self.upp:
                uppvar = transaction.get(uppname)
                if uppvar.min > self.max:
                    self.upp.discard(uppname)
            for lowname in self.low:
                lowvar = transaction.get(lowname)
                lowvar.set_max(max, transaction)

    def set_min(self, min : int, transaction):
        if min > self.min:
            if self.max < min:
                msg = "{} cannot have min {} and max {}."
                raise UnsatisfiabilityError(msg.format(self.id, self.min, self.max))
            self.min = min
            self.modified = True
            for lowname in self.low:
                lowvar = transaction.get(lowname)
                if lowvar.max < self.min:
                    self.low.discard(lowname)
            for uppname in self.upp:
                uppvar = transaction.get(uppname)
                uppvar.set_min(min, transaction)

    def bounds(self, bound, transaction, test = lambda x: True):
        for varname in getattr(self, bound):
            timevar = transaction.get(varname)
            if not test(timevar):
                yield timevar

    def explore_bounds(self, bound, transaction, marker, test = lambda x: True):
        self.explored = marker
        stack = list(self.bounds(bound, transaction, test))
        while len(stack) != 0:
            next_timevar =  stack.pop()
            try:
                explored = (next_timevar.explored == marker)
            except AttributeError:
                explored = False
            if not explored:
                next_timevar.explored = marker
                stack.extend(list(next_timevar.bounds(bound, transaction, test)))
                yield next_timevar

    def set_upp(self, var, transaction):
        pass

    def set_low(self, var, transaction):
        pass

class UnsatisfiabilityError(ValueError):
    pass
        

if __name__ == '__main__':
    timevar1 = TimeVar('name', max = 2)
    dict1 = timevar1.to_json()
    print(dict1)
    timevar2 = TimeVar.from_json(dict1)
    dict2 = timevar2.to_json()
    print(dict2)
