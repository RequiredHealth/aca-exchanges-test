from decimal import Decimal
import json

import requests
import nose

_HOST_UNDER_TEST = ""

def setup_module():
    f = open('test_url.cfg', 'r')
    global _HOST_UNDER_TEST
    _HOST_UNDER_TEST = f.readline().strip()
    f.close() 


class TestPremium:
    def test_orange_county_age_46(self):
        payload = {'lat': '33.74', 'long': '-117.88', 'age': 46}
        r = requests.get(_HOST_UNDER_TEST + '/premium', params=payload)
        # check r.status_code
        result = json.loads(r.content, parse_float=Decimal)
        assert len(result) == 6, 'Got %r results' % len(result)
        print result

    def test_la_county_age_32(self):
        payload = {'lat': '34.07', 'long': '-118.40', 'age': 32}
        r = requests.get(_HOST_UNDER_TEST + '/premium', params=payload)
        # check r.status_code
        result = json.loads(r.content, parse_float=Decimal)
        assert len(result) == 6, 'Got %r results' % len(result)
        print result

    def test_region1_age40(self):
        payload = {'lat': '39.68', 'long': '-122.48', 'age': 40}
        r = requests.get(_HOST_UNDER_TEST + '/premium', params=payload)
        # check r.status_code
        result = json.loads(r.content, parse_float=Decimal)
        print result
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
        nose.tools.assert_almost_equal(result[0]['Premium'], Decimal(239.59), places=1)        
        nose.tools.assert_almost_equal(result[100]['Premium'], Decimal(635.23), places=1)
        print result

    # osceola county
    def test_Kissimmee_FL_age50_zpremium(self):
        payload = {'zip':34741, 'age':50}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        # check r.status_code
        result = json.loads(r.content, parse_float=Decimal)
        assert len(result) == 101, 'Got {} results'.format(len(result))
        nose.tools.assert_almost_equal(result[0]['Premium'], Decimal(239.59), places=1)
        nose.tools.assert_almost_equal(result[100]['Premium'], Decimal(635.23), places=1)

    # hillsborough county
    def test_Tampa_FL_age50(self):
        payload = {'zip':33601, 'age':50}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        # check r.status_code
        result = json.loads(r.content, parse_float=Decimal)
        assert len(result) == 106, 'Got {} results'.format(len(result))
        # todo have a better way to indicate error tolerance than just place of decimals
        nose.tools.assert_almost_equal(result[0]['Premium'], Decimal(219.60), places=1)
        nose.tools.assert_almost_equal(result[105]['Premium'], Decimal(597.61), places=1)

    # hillsborough county
    def test_rating_area_28_FL_age50(self):
        payload = {'state': 'FL', 'rating_area' : 28, 'age' : 50}
        r = requests.get(_HOST_UNDER_TEST + '/ra_premium', params=payload)
        # check r.status_code
        result = json.loads(r.content, parse_float=Decimal)
        assert len(result) == 106, 'Got {} results'.format(len(result))
        # todo have a better way to indicate error tolerance than just place of decimals
        nose.tools.assert_almost_equal(result[0]['Premium'], Decimal(219.60), places=1)
        nose.tools.assert_almost_equal(result[105]['Premium'], Decimal(597.61), places=1)
  
    # miami-dade county
    def test_coconut_grove_FL(self):
        payload = {'zip':33133, 'age':50}
        r = requests.get(_HOST_UNDER_TEST + '/zpremium', params=payload)
        # check r.status_code
        result = json.loads(r.content, parse_float=Decimal)
        assert len(result) == 141, 'Got {} results'.format(len(result))
        # todo have a better way to indicate error tolerance than just place of decimals
        nose.tools.assert_almost_equal(result[0]['Premium'], Decimal(185.72), places=1)
        nose.tools.assert_almost_equal(result[140]['Premium'], Decimal(716.03), places=1)
 
    # miami-dade county
    def test_rating_area_43_FL_age50(self):
        payload = {'state' : 'FL', 'rating_area': 43, 'age':50}
        r = requests.get(_HOST_UNDER_TEST + '/ra_premium', params=payload)
        # check r.status_code
        result = json.loads(r.content, parse_float=Decimal)
        print r.content
        assert len(result) == 141, 'Got {} results'.format(len(result))
        # todo have a better way to indicate error tolerance than just place of decimals
        nose.tools.assert_almost_equal(result[0]['Premium'], Decimal(185.72), places=1)
        nose.tools.assert_almost_equal(result[140]['Premium'], Decimal(716.03), places=1)



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
        print r.content
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
        # returning CA/Butte for all locations outside of california right now
        assert result['state'] == 'CA'
        assert result['county'] == 'BUTTE', 'county returned is %r' % result['county']



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

