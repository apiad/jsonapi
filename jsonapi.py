# coding: utf8

import json


class JsonObj:
    def __init__(self, **kwargs):
        for k,w in kwargs.items():
            setattr(self, str(k), self._parse(w))

    def _json(self, x, query):
        if x is None:
            return None
        if isinstance(x, (int, float, str, bool)):
            return x
        if isinstance(x, (list, tuple)):
            return [self._json(i, query) for i in x]
        if isinstance(x, dict):
            return { str(k): self._json(v) for k,v in x.items() }
        if isinstance(x, JsonObj):
            return x._query(query)
        raise TypeError("type %s is not supported" % type(x))

    def _parse(self, x):
        if x is None:
            return None
        if isinstance(x, (int, float, str, bool)):
            return x
        if isinstance(x, list):
            return [self._parse(i) for i in x]
        if isinstance(x, dict):
            return JsonObj(**x)
        raise TypeError("type %s is not supported" % type(x))

    def _query(self, query):
        if query is None:
            return {key: value for key, value in self.__dict__.items() if not hasattr(value, '__call__')}

        payload = {}

        if isinstance(query, dict):
            items = query.items()
        else:
            items = [(key, None) for key in query]

        for key, value in items:
            attr = getattr(self, key)
            args = {}
            navigation = value

            if isinstance(navigation, dict):
                if "$" in navigation:
                    args = { str(k): self._parse(v) for k,v in navigation.pop("$").items() }
                else:
                    for a in list(navigation.keys()):
                        if a.startswith("$"):
                            v = navigation.pop(a)
                            args[a.strip("$")] = self._parse(v)

            if hasattr(attr, '__call__'):
                result = attr(**args)
            else:
                result = attr

            payload[key] = self._json(result, navigation)

        return payload


class JsonApi(JsonObj):
    def __call__(self, query, encode=False, **kw):
        if isinstance(query, str):
            query = json.loads(query)

        result = self._query(query)

        if encode:
            return json.dumps(result, **kw)

        return result
