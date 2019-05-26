from pytimedb.insertion import Insertion
from pytimedb.memorydb import MemoryDB

import random
import time
import matplotlib.pyplot as plt

def build_inserts(number, max_size, proba_both):
    result = []
    for i in range(number):
        term1 = random.randint(0, max_size)
        term2 = random.randint(0, max_size)
        term1, term2 = min(term1, term2), max(term1, term2)
        if random.random() <= proba_both:
            result.append(['x' + str(term1), 'x' + str(term2)])
        elif random.random() <= 0.5:
            result.append(['x' + str(term1), term2])
        else:
            result.append([term1, 'x'+ str(term2)])
    return result

def test(number, max_size, proba_both):
    database = MemoryDB()
    transaction = Insertion(database)
    inserts = build_inserts(number, max_size, proba_both)
    t1 = time.time()
    result = transaction.can_insert(inserts)
    t2 = time.time()
    return (t2 - t1)

## TEST 1
# results = []
# for i in range(100):
#     results.append(test(10000, 1000, i/100))

# plt.plot(list(range(100)), results, 'ro')
# plt.axis([0, 100, 0, 5])
# plt.show()

## TEST 2
''' results = []
for i in range(100):
    results.append(test(500 * i, 1000, 0.8))

plt.plot(list(range(100)), results, 'ro')
plt.axis([0, 100, 0, 5])
plt.show()
 '''
## TEST 3
results = []
for i in range(100):
    results.append(test(1000 * i, 500, 0.8))

plt.plot(list(range(100)), results, 'ro')
plt.axis([0, 100, 0, 5])
plt.show()
