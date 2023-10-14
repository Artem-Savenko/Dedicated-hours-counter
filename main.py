import sys
import functions

path = sys.argv[1]
activity = sys.argv[2]

functions.collectAllEntries(path)  # must be executed before 'sum_'
functions.sum_(activity, False)