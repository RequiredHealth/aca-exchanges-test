import requests
import nose

class TestPremium:
    host = 'http://localhost:5000'

    def test_all_params(self):
        payload = {'lat': '39.68', 'long': '-122.48', 'age': '25', 'limit':'3'}
        r = requests.get(self.host + '/premium', params=payload)
        # check r.status_code
	result = r.json()
	assert result[0][0] == 'KP_CATA_015'
        assert len(result) == 3, '%r returned' % result


    def test__no_age(self):
        payload = {'lat': '39.68', 'long': '-122.48', 'limit':'3'}
        r = requests.get(self.host + '/premium', params=payload)
        # check r.status_code
        result = r.json()
        assert result['message'] == 'Age is required'

    def test_no_limit(self):
        payload = {'lat': '39.68', 'long': '-122.48', 'age': '25'}
        r = requests.get(self.host + '/premium', params=payload)
        # check r.status_code
        result = r.json()
	assert len(result) == 4, '%r returned' % result

class TestState:
    host = 'http://localhost:5000'

    def test_Artois_CA(self):
        #http://tools.wmflabs.org/geohack/geohack.php?pagename=Artois%2C_California&params=39_37_11_N_122_11_38_W_region:US_type:city
	payload = {'lat': '39.619722', 'long':' -122.193889'}
        r = requests.get(self.host + '/state', params=payload)
        # check r.status_code
        result = r.json()
        assert result['state'] == 'CA'
	assert result['county'] == 'GLENN', 'county returned is %r' % result['county']

    def test_lat39_long122(self):
        payload = {'lat': '39', 'long': '-122'}
        r = requests.get(self.host + '/state', params=payload)
        # check r.status_code
        result = r.json()
        assert result['state'] == 'CA'
        assert result['county'] == 'COLUSA', 'county returned is %r' % result['county']

    def test_TXStateCapitol(self):
        payload = {'lat': '30.274635', 'long': '-97.74039'}
        r = requests.get(self.host + '/state', params=payload)
        # check r.status_code
        result = r.json()
        # returning CA/Butte for all locations outside of california right now
        assert result['state'] == 'CA'
        assert result['county'] == 'BUTTE', 'county returned is %r' % result['county']



class TestRegion:
    host = 'http://localhost:5000'

    def test_CA_butte(self):
        payload = {'state': 'CA', 'county': 'BUTTE'}
        r = requests.get(self.host + '/region', params=payload)
        # check r.status_code
        result = r.json()
        assert result == 1, 'region returned is %r' % result

    def test_CA_napa(self):
        payload = {'state': 'ca', 'county': 'napa'}
        r = requests.get(self.host + '/region', params=payload)
        # check r.status_code
        result = r.json()
        assert result == 2, 'region returned is %r' % result

    def test_TX_travis(self):
        payload = {'state': 'TX', 'county': 'Travis'}
        r = requests.get(self.host + '/region', params=payload)
        # check r.status_code
        result = r.json()
        assert result['message'] == "County Travis doesn't have a matching health region", \
            'region returned is %r' % result


class TestPlan:
    host = 'http://localhost:5000'

    def test_region1_age25_limit2(self):
        payload = {'age': 25, 'region': 1, 'limit': 2}
        r = requests.get(self.host + '/plan', params=payload)
        # check r.status_code
        result = r.json()
        assert result[0][0] == 'KP_CATA_015'
        nose.tools.assert_almost_equal(result[0][1], 202.17, places=2)
        assert len(result) == 2, 'Got %r results' % len(result)

    def test_region1_age40(self):
        payload = {'age': 40, 'region': 1}
        r = requests.get(self.host + '/plan', params=payload)
        # check r.status_code
        result = r.json()
        assert result[1][0] == 'KP_BRNZ_004'
        nose.tools.assert_almost_equal(result[1][1], 261.21, places=2)
        #assert result[0][1] == 257.350159249289, 'returned premium %r' % result[0][1]
        assert len(result) == 4, 'Got %r results' % len(result)


