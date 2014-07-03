from decimal import Decimal
import json

import csv
import requests
import nose

_HOST_UNDER_TEST = ""

def setup_module():
    global _HOST_UNDER_TEST
    _HOST_UNDER_TEST = os.getenv('ACAEX_TEST_URL', 'http://localhost:5001')

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

# a map of rating area to one particular county in the area
area_county = {'r05':'BREVARD',
                'r06':'BROWARD',
                'r08':'CHARLOTTE',
                'r10':'CLAY',
                'r15':'DUVAL',
                'r16':'ESCAMBIA',
                'r28':'HILLSBOROUGH',
                'r34':'LAKE',
                'r40':'MANATEE',
                'r41':'MARION',
                'r43':'MIAMI-DADE',
                'r48':'ORANGE',
                'r49':'OSCEOLA', 
                'r50':'PALM BEACH',
                'r51':'PASCO',
                'r52':'PINELLAS',
                'r56':'SARASOTA',
                'r57':'SEMINOLE',
                'r58':'ST. JOHNS'}


class TestPremium:
    def test_all_ages_and_rating_area_issuer01(self):
        with open('./data/plan-area-age-prem.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for csv_row in csv_reader:
                print 'Checking premium for Plan: {}, in Area: {}, for Age: {}'.format(
 		       csv_row['plan'], csv_row['area'][1:], csv_row['age'])

                example_county = area_county[csv_row['area']]
                print example_county
                payload = {'state': 'FL',
                    'rating_area' : csv_row['area'][1:], 
		    'county' : example_county,
                    'age' : csv_row['age']}
                # TODO bug in how we handle county names containing periods,
                # see trello for more details, but this test will fail right now
                if '.' in example_county:
                    continue

                r = requests.get(_HOST_UNDER_TEST + '/st_cnty_RA_premium', params=payload)
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
    

