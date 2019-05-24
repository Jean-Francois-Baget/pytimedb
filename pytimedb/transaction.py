from pytime.timelinedb import TimeLineDB, TimeLineDBError
from pytime.timevar import TimeVar
 
class Transaction():
    
    def __init__(self, timelinedb : TimeLineDB):
        self.timeline = {}
        self.timelinedb = timelinedb

    def get(self, key : str, create_mode = False):
        try: 
            return self.timeline[key]
        except KeyError:
            try:
                timevar = self.timelinedb.get(key)
                timevar.modified = False
            except TimeLineDBError:
                if create_mode:
                    timevar = TimeVar(key)
                    timevar.modified = True
                else:
                    msg = "{} not present in database, create mode disabled."
                    raise TransactionError(msg.format(key))
            self.timeline[key] = timevar
            return timevar

    def push(self):
        for key in self.timeline:
            timevar = self.timeline[key]
            if timevar.modified:
                self.timelinedb.set(timevar)

class TransactionError(LookupError):
    pass