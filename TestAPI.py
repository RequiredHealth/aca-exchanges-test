from decimal import Decimal
import json

import requests
import nose

_HOST_UNDER_TEST = ""

def setup_module():
    global _HOST_UNDER_TEST
    with open('test_url.cfg', 'r') as f:
        for line in f:
            if line.startswith('#'):
	        continue
            else:
                _HOST_UNDER_TEST = line.strip()
                break

def check_premium(calculated_premium, expected_premium, percent_tolerance=Decimal('0.0001')):
    diff = abs(Decimal(calculated_premium) - expected_premium)
    # check % diff is sufficiently small
    assert diff / expected_premium <= percent_tolerance, \
        'Tolerance ({}) breached. Calculated:{} too far from Expected:{}'.format(
        percent_tolerance * expected_premium, calculated_premium, expected_premium)

FPL = 11490

class TestPremium:
    # can now runs tests like
    #    nosetest --processes=2 TestAPI.py
    # you will only see a speed up though if the backend is run on a 
    # multithreaded server
    _multiprocess_shared_ = True

    def test_orange_county_age_46(self):
        payload = {'lat': '33.74', 'long': '-117.88', 'age': 46}
        r = requests.get(_HOST_UNDER_TEST + '/premium', params=payload)
        # check r.status_code
        result = json.loads(r.content, parse_float=Decimal)
        assert len(result) == 6, 'Got %r results' % len(result)
        #print result

    def test_la_county_age_32(self):
        payload = {'lat': '34.07', 'long': '-118.40', 'age': 32}
        r = requests.get(_HOST_UNDER_TEST + '/premium', params=payload)
        # check r.status_code
        result = json.loads(r.content, parse_float=Decimal)
        assert len(result) == 6, 'Got %r results' % len(result)
        #print result

    def test_region1_age40(self):
        payload = {'lat': '39.68', 'long': '-122.48', 'age': 40}
        r = requests.get(_HOST_UNDER_TEST + '/premium', params=payload)
        # check r.status_code
        result = json.loads(r.content, parse_float=Decimal)
        #print result
        # check 2nd result
        assert result[1]['Insurer'] == 'CA_KFHP',  '%r returned' % result # 'CA_KFHP_005'
        assert result[1]['Plan'] == '005', '%r returned' % result
        nose.tools.assert_almost_equal(result[1]['Premium'], Decimal(258.58), places=2)
        assert len(result) == 6, 'Got %r results' % len(result)

    # osceola county
    def test_Kissimmee_FL_age50(self):
        # Osceola county
        payload = {'lat': '28.283333', 'long': '-81.413222', 'age':50}
        r = requests.get(_HOST_UNDER_TEST + '/premium', params=payload)
        # check r.status_code
        result = json.loads(r.content, parse_float=Decimal)
        assert len(result) == 101, 'Got {} results'.format(len(result))
        check_premium(result[0]['Premium'], Decimal('239.59'))        
        check_premium(result[100]['Premium'], Decimal('635.23'))
        #print result

    # osceola county
    def test_Kissimmee_FL_age50_zpremium(self):
        payload = {'zip':34741, 'age':50}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        # check r.status_code
        result = json.loads(r.content, parse_float=Decimal)
        assert len(result) == 101, 'Got {} results'.format(len(result))
        check_premium(result[0]['Premium'], Decimal('239.59'))
        check_premium(result[100]['Premium'], Decimal('635.23'))

    # hillsborough county
    def test_Tampa_FL_age50(self):
        payload = {'zip':33601, 'age':50}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        # check r.status_code
        result = json.loads(r.content, parse_float=Decimal)
        assert len(result) == 106, 'Got {} results'.format(len(result))
        check_premium(result[0]['Premium'], Decimal('219.60'))
        check_premium(result[105]['Premium'], Decimal('597.61'))


    # travis county
    def test_Austin_TX_age50(self):
        payload = {'zip':78731, 'age':50}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        # check r.status_code
        result = json.loads(r.content, parse_float=Decimal)
        assert len(result) == 80, 'Got {} results'.format(len(result))
        check_premium(result[0]['Premium'], Decimal('185.83'), Decimal('0.0005'))
        check_premium(result[79]['Premium'], Decimal('569.66'))

    

    def test_Austin25(self):
        payload = {'zip':78731, 'age':25, 'limit_catastrophic': True}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        assert result[0]['Tier'] == 'Catastrophic'
        for res in result:
            assert res['Premium'] > Decimal(0)
            assert res.get('Deductible') >= 0, 'Missing deductible: {}'.format(res)

    def test_Austin30(self):
        payload = {'zip':78731, 'age':30, 'limit_catastrophic': True}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        assert result[0]['Tier'] == 'Bronze', 'Got {} expected Bronze'.format(result[0]['Tier'])
        for res in result:
            assert res['Premium'] > Decimal(0)
            assert res['Tier'] != 'Catastrophic'
            if res['Plan'] == 'Blue Advantage Silver HMO 003':
                assert res['Deductible'] == 6000

    def test_Austin25_5xFPL(self):
        payload = {'zip':78731, 'age':25, 'limit_catastrophic': True, 
            'household_income': 5 * FPL, 'household_size': 1}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        assert result[0]['Tier'] == 'Catastrophic'
        for res in result:
            assert res['Premium'] > Decimal(0)
            assert res.get('Deductible') >= 0, 'Missing deductible: {}'.format(res)

    def test_Austin30_5xFPL(self):
        payload = {'zip':78731, 'age':30, 'limit_catastrophic': True,
            'household_income': 5 * FPL, 'household_size': 1}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        assert result[0]['Tier'] == 'Bronze', 'Got {} expected Bronze'.format(result[0]['Tier'])
        for res in result:
            assert res['Premium'] > Decimal(0)
            assert res['Tier'] != 'Catastrophic'
            if res['Plan'] == 'Blue Advantage Silver HMO 003':
                assert res['Deductible'] == 6000


    def test_Austin25_1xFPL(self):
        payload = {'zip':78731, 'age':25, 'limit_catastrophic': True,
            'household_income': 1 * FPL, 'household_size': 1}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        # in theory this could be silver because the are likely to be both silver
        # and bronze plans where the premiums are zero after subsidy
        assert result[0]['Tier'] == 'Bronze', 'Got {} expected Bronze'.format(result[0]['Tier'])
        assert result[0]['Premium'] == Decimal(0)
        prev_premium = -1
        for res in result:
            # make sure results are sorted by premium asc
            res['Premium'] >= prev_premium
            prev_premium == res['Premium'] 
            if res['Tier'] == 'Catastrophic':
                assert res['Premium'] > Decimal('0')
            assert res.get('Deductible') >= 0, 'Missing deductible: {}'.format(res)

    def test_CentralTexas25_1xFPL(self):
        # Travis county
        payload = {'zip':78731, 'age':25, 'limit_catastrophic': True,
            'household_income': 1 * FPL, 'household_size': 1}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        for res in result:
            assert res.get('Deductible') >= 0, 'Missing deductible: {}'.format(res)

        # Bastrop county
        payload = {'zip':78602, 'age':25, 'limit_catastrophic': True,
            'household_income': 1 * FPL, 'household_size': 1}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        for res in result:
            assert res.get('Deductible') >= 0, 'Missing deductible: {}'.format(res)

        # Blanco county
        payload = {'zip':78070, 'age':25, 'limit_catastrophic': True,
            'household_income': 1 * FPL, 'household_size': 1}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        for res in result:
            assert res.get('Deductible') >= 0, 'Missing deductible: {}'.format(res)

        # Burnet county
        payload = {'zip':73301, 'age':25, 'limit_catastrophic': True,
            'household_income': 1 * FPL, 'household_size': 1}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        for res in result:
            assert res.get('Deductible') >= 0, 'Missing deductible: {}'.format(res)

        # Caldwell county
        payload = {'zip':78610, 'age':25, 'limit_catastrophic': True,
            'household_income': 1 * FPL, 'household_size': 1}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        for res in result:
            assert res.get('Deductible') >= 0, 'Missing deductible: {}'.format(res)

        # Comal county
        payload = {'zip':78602, 'age':25, 'limit_catastrophic': True,
            'household_income': 1 * FPL, 'household_size': 1}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        for res in result:
            assert res.get('Deductible') >= 0, 'Missing deductible: {}'.format(res)


        # Williamson county
        payload = {'zip':78646, 'age':25, 'limit_catastrophic': True,
            'household_income': 1 * FPL, 'household_size': 1}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        for res in result:
            assert res.get('Deductible') >= 0, 'Missing deductible: {}'.format(res)

        # Fayette county
        payload = {'zip':78932, 'age':25, 'limit_catastrophic': True,
            'household_income': 1 * FPL, 'household_size': 1}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        for res in result:
            assert res.get('Deductible') >= 0, 'Missing deductible: {}'.format(res)

        # Gillespie county
        payload = {'zip':76856, 'age':25, 'limit_catastrophic': True,
            'household_income': 1 * FPL, 'household_size': 1}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        for res in result:
            assert res.get('Deductible') >= 0, 'Missing deductible: {}'.format(res)

        # Hays county
        payload = {'zip':78620, 'age':25, 'limit_catastrophic': True,
            'household_income': 1 * FPL, 'household_size': 1}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        for res in result:
            assert res.get('Deductible') >= 0, 'Missing deductible: {}'.format(res)

        # Lee county
        payload = {'zip':76578, 'age':25, 'limit_catastrophic': True,
            'household_income': 1 * FPL, 'household_size': 1}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        for res in result:
            assert res.get('Deductible') >= 0, 'Missing deductible: {}'.format(res)

        # Llano county
        payload = {'zip':76831, 'age':25, 'limit_catastrophic': True,
            'household_income': 1 * FPL, 'household_size': 1}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        for res in result:
            assert res.get('Deductible') >= 0, 'Missing deductible: {}'.format(res)


    def test_Austin30_1xFPL(self):
        payload = {'zip':78731, 'age':30, 'limit_catastrophic': True,
            'household_income': 1 * FPL, 'household_size': 1}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        # in theory this could be silver because the are likely to be both silver
        # and bronze plans where the premiums are zero after subsidy
        assert result[0]['Tier'] == 'Bronze', 'Got {} expected Bronze'.format(result[0]['Tier'])
        assert result[0]['Premium'] == Decimal(0)
        prev_premium = -1
        for res in result:
            # make sure results are sorted by premium asc
            res['Premium'] >= prev_premium
            prev_premium == res['Premium']
            assert res['Tier'] != 'Catastrophic'
            if res['Plan'] == 'Blue Advantage Silver HMO 003':
               assert res['Deductible'] == 500

    def test_Austin30_2xFPL(self):
        payload = {'zip':78731, 'age':30, 'limit_catastrophic': True,
            'household_income': 2 * FPL, 'household_size': 1}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        # in theory this could be silver because the are likely to be both silver
        # and bronze plans where the premiums are zero after subsidy
        for res in result:
            assert res.get('Deductible') >= 0, 'Missing deductible: {}'.format(res)
            if res['Plan'] == 'Blue Advantage Silver HMO 003':
               assert res['Deductible'] == 1500


    def test_Austin30_2pt4xFPL(self):
        payload = {'zip':78731, 'age':30, 'limit_catastrophic': True,
            'household_income': int(2.4 * FPL), 'household_size': 1}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        # in theory this could be silver because the are likely to be both silver
        # and bronze plans where the premiums are zero after subsidy
        for res in result:
            assert res.get('Deductible') >= 0, 'Missing deductible: {}'.format(res)
            if res['Plan'] == 'Blue Advantage Silver HMO 003':
               assert res['Deductible'] == 5000

    def test_Austin30_pt4xFPL(self):
        payload = {'zip':78731, 'age':30, 'limit_catastrophic': True,
            'household_income': int(0.4 * FPL), 'household_size': 1}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        result = json.loads(r.content, parse_float=Decimal)
        # in theory this could be silver because the are likely to be both silver
        # and bronze plans where the premiums are zero after subsidy
        for res in result:
            assert res.get('Deductible') >= 0, 'Missing deductible: {}'.format(res)
            if res['Plan'] == 'Blue Advantage Silver HMO 003':
               assert res['Deductible'] == 6000


    def test_Boston_MA_age50(self):
        payload = {'zip':02201, 'age':50}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        # check r.status_code
        assert r.status_code == 404

    # Gundersen Health Plan, Inc does NOT offer plans in Linn county (rating area 6)
    def test_Linn_county__IA_age50(self):
        # Cedar rapids is in Linn county
        payload = {'zip':52401, 'age':50}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        # check r.status_code
        result = json.loads(r.content, parse_float=Decimal)
        print result
        assert len(result) == 35, 'Got {} results'.format(len(result))
        check_premium(result[0]['Premium'], Decimal('153.55'))
        check_premium(result[34]['Premium'], Decimal('582.70'))

    # Gundersen Health Plan, Inc does offer plans in Clayton county (rating area 6)
    def test_Clayton_county_IA_age50(self):
        # Elkader is in Clayton county
        payload = {'zip':52043, 'age':50}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        # check r.status_code
        result = json.loads(r.content, parse_float=Decimal)
        print result
        assert len(result) == 46, 'Got {} results'.format(len(result))
        check_premium(result[0]['Premium'], Decimal('193.29'), Decimal('0.0005'))
        check_premium(result[45]['Premium'], Decimal('710.01'))


    # hillsborough county
    def test_Tampa_FL_age50(self):
        # tampa
        payload = {'zip' : 33660, 'age' : 50}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        # check r.status_code
        result = json.loads(r.content, parse_float=Decimal)
        assert len(result) == 106, 'Got {} results'.format(len(result))
        # todo have a better way to indicate error tolerance than just place of decimals
        check_premium(result[0]['Premium'], Decimal('219.60'))
        check_premium(result[105]['Premium'], Decimal('597.61'))

#dupe  
    # miami-dade county
#    def test_coconut_grove_FL(self):
#        payload = {'zip':33133, 'age':50}
#        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
#        # check r.status_code
#        result = json.loads(r.content, parse_float=Decimal)
#        assert len(result) == 141, 'Got {} results'.format(len(result))
#        # todo have a better way to indicate error tolerance than just place of decimals
#        nose.tools.assert_almost_equal(result[0]['Premium'], Decimal(185.72), places=1)
#        nose.tools.assert_almost_equal(result[140]['Premium'], Decimal(716.03), places=1)
 

    # miami-dade county
    def test_33101_age50(self):
        # miami
        payload = {'zip' : 33101, 'age':50}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        # check r.status_code
        result = json.loads(r.content, parse_float=Decimal)
        #print r.content
        assert len(result) == 141, 'Got {} results'.format(len(result))
        # todo have a better way to indicate error tolerance than just place of decimals
        check_premium(result[0]['Premium'], Decimal('185.72'))
        check_premium(result[140]['Premium'], Decimal('716.03'))



    def test_non_existent_zip(self):
        payload = {'zip':99999, 'age':50}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        # check r.status_code
        assert r.status_code == 404

# with more insurers now, there should be no zips without coverage    
#    def test_valid_zip_with_no_coverage(self):
#        payload = {'zip':32601, 'age':50}
#        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
#        # check r.status_code
#        assert r.status_code == 404, r.content


    def test_all_params(self):
        payload = {'lat': '39.68', 'long': '-122.48', 'age': '25', 'limit':'3'}
        r = requests.get(_HOST_UNDER_TEST + '/premium', params=payload)
        # check r.status_code
        #print r.content
        result = json.loads(r.content, parse_float=Decimal)	
        assert result[0]['Insurer'] == 'CA_KFHP'  # 'CA_KFHP_015'
        assert result[0]['Plan'] == '015'
        nose.tools.assert_almost_equal(result[0]['Premium'], Decimal(202.17), places=2)
        assert len(result) == 3, '%r returned' % result

    def test__no_age(self):
        payload = {'lat': '39.68', 'long': '-122.48', 'limit':'3'}
        r = requests.get(_HOST_UNDER_TEST + '/premium', params=payload)
        # check r.status_code
        result = r.json()
        assert result['message'] == 'Age is required'

    def test_no_limit(self):
        payload = {'lat': '39.68', 'long': '-122.48', 'age': '25'}
        r = requests.get(_HOST_UNDER_TEST + '/premium', params=payload)
        # check r.status_code
        result = r.json()
	assert len(result) == 6, '%r returned' % result



class TestState:
    def test_Artois_CA(self):
        #http://tools.wmflabs.org/geohack/geohack.php?pagename=Artois%2C_California&params=39_37_11_N_122_11_38_W_region:US_type:city
	payload = {'lat': '39.619722', 'long':'-122.193889'}
        r = requests.get(_HOST_UNDER_TEST + '/state', params=payload)
        # check r.status_code
        result = r.json()
        assert result['state'] == 'CA'
	assert result['county'] == 'GLENN', 'county returned is %r' % result['county']

    def test_lat39_long122(self):
        payload = {'lat': '39', 'long': '-122'}
        r = requests.get(_HOST_UNDER_TEST + '/state', params=payload)
        # check r.status_code
        result = r.json()
        assert result['state'] == 'CA'
        assert result['county'] == 'COLUSA', 'county returned is %r' % result['county']

    def test_orange_county(self):
        payload = {'lat': '33.74', 'long': '-117.88'}
        r = requests.get(_HOST_UNDER_TEST + '/state', params=payload)
        # check r.status_code
        result = r.json()
        assert result['state'] == 'CA'
        assert result['county'] == 'ORANGE', 'county returned is %r' % result['county']

    def test_la_county(self):
        payload = {'lat': '34.07', 'long': '-118.40'}
        r = requests.get(_HOST_UNDER_TEST + '/state', params=payload)
        # check r.status_code
        result = r.json()
        assert result['state'] == 'CA'
        assert result['county'] == 'LOS ANGELES', 'county returned is %r' % result['county']


    def test_TXStateCapitol(self):
        payload = {'lat': '30.274635', 'long': '-97.74039'}
        r = requests.get(_HOST_UNDER_TEST + '/state', params=payload)
        # check r.status_code
        result = r.json()
        assert result['state'] == 'TX'
        assert result['county'] == 'TRAVIS', 'county returned is %r' % result['county']



class TestRegion:
    def test_CA_butte(self):
        payload = {'state': 'CA', 'county': 'BUTTE'}
        r = requests.get(_HOST_UNDER_TEST + '/region', params=payload)
        # check r.status_code
        result = r.json()
        assert result == 1, 'region returned is %r' % result

    def test_CA_la(self):
        payload = {'state': 'CA', 'county': 'LOS ANGELES'}
        r = requests.get(_HOST_UNDER_TEST + '/region', params=payload)
        # check r.status_code
        result = r.json()
        assert result == 16, 'region returned is %r' % result

    def test_CA_orange(self):
        payload = {'state': 'CA', 'county': 'ORANGE'}
        r = requests.get(_HOST_UNDER_TEST + '/region', params=payload)
        # check r.status_code
        result = r.json()
        assert result == 18, 'region returned is %r' % result

    def test_CA_napa(self):
        payload = {'state': 'ca', 'county': 'napa'}
        r = requests.get(_HOST_UNDER_TEST + '/region', params=payload)
        # check r.status_code
        result = r.json()
        assert result == 2, 'region returned is %r' % result

    def test_TX_travis(self):
        payload = {'state': 'TX', 'county': 'Travis'}
        r = requests.get(_HOST_UNDER_TEST + '/region', params=payload)
        # check r.status_code
        result = r.json()
        assert result['message'] == "County Travis doesn't have a matching health region", \
            'region returned is %r' % result

