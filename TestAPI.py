import requests

class TestAPI:
    def test_c(self):
        assert 'c' == 'c'
        payload = {'lat': '39.68', 'long': '-122.48', 'age': '25', 'limit':'3'}
        r = requests.get('http://localhost:5000/premium', params=payload)
        # check r.status_code
	result = r.json()
	assert result[0][0] == 'KP_CATA_015'
