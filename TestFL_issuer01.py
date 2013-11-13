from decimal import Decimal
import json

import csv
import requests
import nose

_HOST_UNDER_TEST = ""

def setup_module():
    f = open('test_url.cfg', 'r')
    global _HOST_UNDER_TEST
    _HOST_UNDER_TEST = f.readline().strip()
    f.close() 

def check_premium(expected_premium, actual_premium, tolerance):
    diff = abs(Decimal(expected_premium) - actual_premium)
    # check % diff is sufficiently small
    assert diff / actual_premium <= tolerance, \
        'Tolerance breached. Actual:{} too far from Expected:{}'.format(
             actual_premium, expected_premium)

plan_name_id_map = {'p04': 'Aetna Basic',
                    'p02': 'Aetna Advantage 6350',
                    'p03': 'Aetna AdvantagePlus 5500 PD',
                    'p01': 'Aetna Advantage 5750 PD',
                    'p07': 'Aetna Classic 5000',
                    'p06': 'Aetna Classic 3500 PD',
                    'p05': 'Aetna Premier 2000 PD'
                     }


class TestPremium:
    def test_all_ages_and_rating_area_issuer01(self):
        with open('./data/plan-area-age-prem.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for csv_row in csv_reader:
                print 'Checking premium for Plan: {}, in Area: {}, for Age: {}'.format(
 		       csv_row['plan'], csv_row['area'][1:], csv_row['age'])

                payload = {'state': 'FL',
                    'rating_area' : csv_row['area'][1:], 
                    'age' : csv_row['age']}
                r = requests.get(_HOST_UNDER_TEST + '/ra_premium', params=payload)
                # check r.status_code
                result = json.loads(r.content, parse_float=Decimal)
                plan_name = plan_name_id_map[csv_row['plan']]
                # print result
                for query_row in result:
                    print 'checking {} and {}'.format( query_row['Insurer'], query_row['Plan'])
                    if query_row['Insurer'] == 'Aetna' and \
                            query_row['Plan'] == plan_name:
                        print 'found it'
                        # check actual and calculated differ by < x%
 		        check_premium(csv_row['premium'], query_row['Premium'], 0.01)
		        break
		else:
		    continue
    

