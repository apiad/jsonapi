import json
from jsonapi import JsonApi, JsonObj


def test_api_input_string():
    class TestApi(JsonApi):
        def something(self, a, b):
            return a.x + b.y

    api = TestApi()
    query = {
        'something': {
            '$a': {'x': 10},
            '$b': {'y': 20},
        }
    }

    expected_response = {
        'something': 30
    }

    query_str = json.dumps(query)

    assert api(query) == expected_response
    assert api(query) == api(query_str)
    assert json.dumps(api(query), sort_keys=True) == api(query, encode=True, sort_keys=True)
