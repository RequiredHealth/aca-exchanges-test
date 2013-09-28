import requests

class TestPremium:
    host = 'http://localhost:5000'

    def test_premium_all_params(self):
        payload = {'lat': '39.68', 'long': '-122.48', 'age': '25', 'limit':'3'}
        r = requests.get(self.host + '/premium', params=payload)
        # check r.status_code
	result = r.json()
	assert result[0][0] == 'KP_CATA_015'

    def test_premium_no_age(self):
        payload = {'lat': '39.68', 'long': '-122.48', 'limit':'3'}
        r = requests.get(self.host + '/premium', params=payload)
        # check r.status_code
        result = r.json()
        assert result['message'] == 'Age is required'

    def test_premium_no_limit(self):
        payload = {'lat': '39.68', 'long': '-122.48', 'age': '25'}
        r = requests.get(self.host + '/premium', params=payload)
        # check r.status_code
        result = r.json()
        # TODO uncomment when working	
	#assert len(result) == 4, 'There should be 4 results in the list'

class TestState:
    host = 'http://localhost:5000'

    def test_state_county_CA_glenn(self):
        payload = {'lat': '39.68', 'long': '-122.48'}
        r = requests.get(self.host + '/state', params=payload)
        # check r.status_code
        result = r.json()
        assert result['state'] == 'CA'
	assert result['county'] == 'GLENN', 'county returned is %r' % result['county']

    def test_state_county_CA_colusa(self):
        payload = {'lat': '39', 'long': '-122'}
        r = requests.get(self.host + '/state', params=payload)
        # check r.status_code
        result = r.json()
        assert result['state'] == 'CA'
        assert result['county'] == 'COLUSA', 'county returned is %r' % result['county']

    def test_state_county_TX_austin(self):
        payload = {'lat': '30.274635', 'long': '-97.74039'}
        r = requests.get(self.host + '/state', params=payload)
        # check r.status_code
        result = r.json()
        assert result['state'] == 'CA'
        assert result['county'] == 'BUTTE', 'county returned is %r' % result['county']

