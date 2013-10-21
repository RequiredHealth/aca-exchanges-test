import csv

with open('premium-orig.csv', 'rb') as f:
    reader = csv.reader(f)
    i = 0
    for row in reader:
        # determine what sort of row do we have
        # its either DD or DDDD
        # if its not one of those those we should bomb out

        # only process none empty rows
        if row:
            val = row[0]
            i += 1
            # covers DD.00 and DDD.00
            if len(val) == 5 or len(val) == 6:
                print val
            # covers DD.00DDD.00, DDD.00DD.00, DD.00DDD.00 and DDD.00DDD.00
            elif len(val) >= 10 or len(val) <= 12:
                firstdp = val.find('.')
                if firstdp == -1:
                    raise Exception("Badly formatted row {0}, value {1}".format(i,val))
                print val[:firstdp + 3]
                i += 1
                print val[firstdp + 3:]
            else:
                raise Exception("Badly formatted row {0}, value {1}".format(i,val))
