# coding: utf-8

import json
from jsonapi import JsonApi, JsonObj


class A:
    pass


class SampleApi(JsonApi):
    def something(self, a, b):
        return a.x + b.y

    def null(self):
        return None

    def dictionary(self):
        return {1: {2: 3}}

    def not_supported(self):
        return A()


def test_api_return_null():
    api = SampleApi()
    assert api({'null'}) == {'null': None}


def test_api_return_dict():
    api = SampleApi()
    assert api({'dictionary'}) == {'dictionary': {'1': {'2': 3}}}


def test_api_return_not_supported():
    api = SampleApi()

    try:
        api({'not_supported'})
        assert False # pragma: no cover
    except TypeError as e:
        assert 'is not supported' in str(e)


def test_api_return_not_supported_query():
    api = SampleApi()

    try:
        api({'not_supported': {'$x': A()}})
        assert False # pragma: no cover
    except TypeError as e:
        assert 'is not supported' in str(e)


def test_jsonobj_repr():
    obj = JsonObj(a={'b': 42})
    assert str(obj) == "JsonObj({'a': {'b': 42}})"


def test_jsonobj_serialize_wrong_type():
    try:
        obj = JsonObj(a=A())
        assert False # pragma: no cover
    except TypeError as e:
        assert 'is not supported' in str(e)

    obj = JsonObj()
    obj.b = A()

    try:
        obj.json()
        assert False # pragma: no cover
    except TypeError as e:
        assert 'is not supported' in str(e)


def test_api_input_string():
    api = SampleApi()
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


class Person(JsonObj):
    first_name = ""
    last_name = ""

    def __init__(self, first_name: str, last_name: str):
        super(Person, self).__init__(first_name=first_name, last_name=last_name)

    def fullname(self):
        return "%s %s" % (self.first_name, self.last_name)


class PersonApi(JsonApi):
    def name_it(self, title, person: Person):
        return "%s %s" % (title, person.fullname())


def test_parse_args():
    api = PersonApi()
    r = api({ 'name_it': {'$person': {'first_name': 'John',
                                      'last_name': 'Doe' },
                          '$title': 'Mr.'}})

    assert r == {'name_it': 'Mr. John Doe'}
