import csv
from decimal import Decimal 

with open('age-proc.csv', 'rb') as f:
    reader = csv.reader(f)
    i = 0
    run = 0
    MIN_RUN = 45
    prev = 0 
    for row in reader:
        # only process none empty rows
        if row:
            curr = Decimal(row[0])
            i += 1
            # do we continue the run or start a new one
            if curr >= prev:
                run += 1
            else: # start a new run
                if run < MIN_RUN: # if run isnt long enough                
                    raise Exception("Run wasn't long enough, only {0} values, ending with id {1}. Last values {2} and {3}".format(run, i, prev, curr))
                run = 0 
            prev = curr

