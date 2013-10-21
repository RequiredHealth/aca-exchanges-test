import csv
from decimal import Decimal 
from collections import deque

with open('age-proc.csv', 'rb') as f:
    reader = csv.reader(f)
    i = 0
    age_q = deque()

    for row in reader:
        # only process none empty rows
        if row:
            age_q.append(int(row[0]))
            i += 1

with open('premium-proc.csv', 'rb') as f:
    reader = csv.reader(f)
    i = 0
    prem_q = deque()

    for row in reader:
        # only process none empty rows
        if row:
            prem_q.append(Decimal(row[0]))
            i += 1

def getAge(id):
    return (id % 46) + 20

def getPlanId(id):
    planIds = ['p01','p02',None,'p03','p04',None,'p05','p06','p07',None]
    #return 'p' + str((id / 874) + 1)
    return planIds[id/874]
 
def getRatingAreaId(id):
    areaIds = ['r10','r15','r16','r28','r34','r40','r41','r43','r48','r49','r05',
               'r50','r51','r52','r56','r57','r58','r06','r08']
    return areaIds[(id /46) % 19]

fillin_premiums = {3447: Decimal(596.00),
                   3713: Decimal(313.00),
                   3979: Decimal(191.00),
                   4245: Decimal(189.00),
                   4511: Decimal(154.00),
                   4776: Decimal(417.00),
                   4777: Decimal(426.00),
                   5043: Decimal(249.00),
                   5309: Decimal(401.00),
                   5574: Decimal(325.00),
                   5575: Decimal(334.00),
                   5840: Decimal(868.00),
                   5841: Decimal(868.00),
                   6107: Decimal(615.00),
                   6373: Decimal(359.00),
                   6637: Decimal(313.00),
                   6638: Decimal(317.00),
                   6639: Decimal(319.00),
                   6903: Decimal(261.00),
                   6904: Decimal(261.00),
                   6905: Decimal(262.00),
                   7169: Decimal(630.00),
                   7170: Decimal(657.00),
                   7171: Decimal(680.00),
                   7435: Decimal(440.00),
                   7436: Decimal(460.00),
                   7437: Decimal(481.00),
                   7701: Decimal(325.00),
                   7702: Decimal(329.00),
                   7703: Decimal(336.00),
                   7967: Decimal(234.00),
                   7968: Decimal(237.00),
                   7969: Decimal(242.00),
                   8233: Decimal(774.00),
                   8234: Decimal(170.00),
                   8235: Decimal(268.00),
                   8499: Decimal(561.00),
                   8500: Decimal(587.00),
                   8501: Decimal(613.00)}

def getPremium(id):
    next_age = age_q.popleft()
    # we are missing some data
    if getAge(id) != next_age:
       # put the age back so we can process it later
       age_q.appendleft(next_age)
       # and get the data from our store
       try:
           return fillin_premiums[id]
       except KeyError, e:
           # we haven't filled this premium in yet, so lets give some good info on what's needed
           print 'Need to lookup premium for plan:{0}, rating area {1}, age {2}, id {3}. Next age value is {4}'.format(getPlanId(id), getRatingAreaId(id), getAge(id), id, next_age)
           raise
    else:
       return prem_q.popleft()



assert getAge(0) == 20
assert getAge(45) == 65
assert getAge(8739) == 65
assert getAge(873) == 65
assert getAge(874) == 20
assert getPlanId(0) == 'p01'
assert getPlanId(1) == 'p01'
assert getPlanId(46) == 'p01'

assert getPlanId(872) == 'p01' # p1,r8,a64
assert getRatingAreaId(872) == 'r08'
assert getAge(872) == 64

assert getPlanId(873) == 'p01' # p1,r8,a65

assert getPlanId(874) == 'p02' # p2,r10,a20
assert getRatingAreaId(874) == 'r10'
assert getAge(874) == 20

assert getPlanId(875) == 'p02' # p2,r10,a21
assert getRatingAreaId(875) == 'r10'
assert getAge(875) == 21

assert getPlanId(8739) == None
assert getRatingAreaId(8739) == 'r08'
assert getAge(8739) == 65

for i in range(0, 8740):
    planId = getPlanId(i)
    areaId = getRatingAreaId(i)
    age = getAge(i)
    premium = getPremium(i)
    # skip data which doesnt match an actual plan
    if planId:
        print '{0},{1},{2},{3},{4}'.format(i, planId, areaId, age, premium)


