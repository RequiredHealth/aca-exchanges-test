# imports for managing json parsing
from collections import OrderedDict
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
    def test_region1_age40(self):
        payload = {'lat': '39.68', 'long': '-122.48', 'age': 40}
        r = requests.get(_HOST_UNDER_TEST + '/premium', params=payload)
        # check r.status_code
        result = json.loads(r.content, object_pairs_hook=OrderedDict, parse_float=Decimal)
        assert result.keys()[1] == 'CA_KFHP_005', '%r returned' % result
        #assert result[1][0] == 'CA_KFHP_005', '%r returned' % result
        nose.tools.assert_almost_equal(result[result.keys()[1]], Decimal(258.58), places=2)
        #nose.tools.assert_almost_equal(result[1][1], 258.58, places=2)
        assert len(result) == 8, 'Got %r results' % len(result)

    def test_all_params(self):
        payload = {'lat': '39.68', 'long': '-122.48', 'age': '25', 'limit':'3'}
        r = requests.get(_HOST_UNDER_TEST + '/premium', params=payload)
        # check r.status_code
        result = json.loads(r.content, object_pairs_hook=OrderedDict, parse_float=Decimal)	
        assert result.keys()[0] == 'CA_KFHP_015'
        #assert result[0][0] == 'CA_KFHP_015'
        nose.tools.assert_almost_equal(result[result.keys()[0]], Decimal(202.17), places=2)
        #nose.tools.assert_almost_equal(result[0][1], 202.17, places=2)
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
	assert len(result) == 8, '%r returned' % result



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

