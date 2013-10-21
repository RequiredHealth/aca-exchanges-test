import csv
from decimal import Decimal 

area_factors = {'r05':Decimal(0.807342232676000),
                'r06':Decimal(0.823652176841000),
                'r08':Decimal(0.785595640456000),
                'r10':Decimal(0.905201897667000),
                'r15':Decimal(0.905201897667000), # note same aa above
                'r16':Decimal(0.687735975465000),
                'r28':Decimal(0.826370500869000),
                'r34':Decimal(0.880736981419000),
                'r40':Decimal(0.785595640456000),
                'r41':Decimal(0.913356869749000),
                'r43':Decimal(0.850835417116000),
                'r48':Decimal(0.880736981419000),
                'r49':Decimal(0.880736981419000), # note same as above
                'r50':Decimal(0.823652176841000),
                'r51':Decimal(0.826370500869000),
                'r52':Decimal(0.826370500869000), # note same as above
                'r56':Decimal(0.785595640456000),
                'r57':Decimal(0.880736981419000),
                'r58':Decimal(0.905201897667000)}

plan_factors = {'p01':Decimal(1.270543416760000),
                'p02':Decimal(1.199629365630000),
                'p03':Decimal(1.223267382670000),
                'p04':Decimal(0.874606631300000),
                'p05':Decimal(1.755122766120000),
                'p06':Decimal(1.583747142570000),
                'p07':Decimal(1.465557057360000)}


age_factors = {20:Decimal(0.635),
               21:Decimal(1.000),
               22:Decimal(1.000),
               23:Decimal(1.000),
               24:Decimal(1.000),
               25:Decimal(1.004),
               26:Decimal(1.024),
               27:Decimal(1.048),
               28:Decimal(1.087),
               29:Decimal(1.119),
               30:Decimal(1.135),
               31:Decimal(1.159),
               32:Decimal(1.183),
               33:Decimal(1.198),
               34:Decimal(1.214),
               35:Decimal(1.222),
               36:Decimal(1.230),
               37:Decimal(1.238),
               38:Decimal(1.246),
               39:Decimal(1.262),
               40:Decimal(1.278),
               41:Decimal(1.302),
               42:Decimal(1.325),
               43:Decimal(1.357),
               44:Decimal(1.397),
               45:Decimal(1.444),
               46:Decimal(1.500),
               47:Decimal(1.563),
               48:Decimal(1.635),
               49:Decimal(1.706),
               50:Decimal(1.786),
               51:Decimal(1.865),
               52:Decimal(1.952),
               53:Decimal(2.040),
               54:Decimal(2.135),
               55:Decimal(2.230),
               56:Decimal(2.333),
               57:Decimal(2.437),
               58:Decimal(2.548),
               59:Decimal(2.603),
               60:Decimal(2.714),
               61:Decimal(2.810),
               62:Decimal(2.873),
               63:Decimal(2.952),
               64:Decimal(3.000),
               65:Decimal(3.000)}


with open('plan-area-age-prem.csv', 'rb') as f:
    reader = csv.DictReader(f)
    i = 0
    max_diff = 0
    max_diff_id = 0
    max_perc_diff = 0
    max_perc_diff_id = 0
    for row in reader:
        # only process none empty rows
        if row:
            calc_premium = plan_factors[row['plan']]*area_factors[row['area']]*age_factors[int(row['age'])]*200
            premium_diff = abs(Decimal(row['premium']) - calc_premium)
            premium_diff_perc = premium_diff/Decimal(row['premium'])
            if premium_diff > max_diff:
                max_diff = premium_diff
                max_diff_id = row['id']
            if premium_diff_perc > max_perc_diff:
                max_perc_diff = premium_diff_perc
                max_perc_diff_id = row['id']

            i += 1

    print 'Max diff is ${0}, id {1}'.format(max_diff, max_diff_id)
    print 'Max % diff is {0}%, id {1}'.format(max_perc_diff*100, max_perc_diff_id)

