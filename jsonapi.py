# coding: utf8

import json


class JsonObj:
    def __init__(self, **kwargs):
        for k,w in kwargs.items():
            setattr(self, str(k), self._parse(w))

    def dict(self):
        return {key: self._json(value) for key, value in self.__dict__.items() if not hasattr(value, '__call__')}

    def json(self, **kwargs):
        return json.dumps(self.dict(), **kwargs)

    def _json(self, x):
        if x is None:
            return None
        if isinstance(x, (int, float, str, bool)):
            return x
        if isinstance(x, (list, tuple)):
            return [self._json(i) for i in x]
        if isinstance(x, dict):
            return { str(k): self._json(v) for k,v in x.items() }
        if isinstance(x, JsonObj):
            return x.dict()

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

    @staticmethod
    def from_json(s):
        return JsonObj(**json.loads(s))


class JsonApi(JsonObj):
    def _query(self, obj, query):
        if obj is None:
            return None

        if isinstance(obj, (int, float, str, bool)):
            return obj

        if isinstance(obj, (list, tuple)):
            return [self._query(i, query) for i in obj]

        if isinstance(obj, dict):
            return {str(k): self._query(v, query) for k, v in obj.items()}

        if isinstance(obj, JsonObj):
            if query is None:
                return {key: value for key, value in obj.__dict__.items() if not hasattr(value, '__call__')}

            payload = {}

            if isinstance(query, dict):
                items = query.items()
            else:
                items = [(key, None) for key in query]

            for key, value in items:
                attr = getattr(obj, key)
                args = {}
                navigation = value

                if isinstance(navigation, dict):
                    if "$" in navigation:
                        args = {str(k): self._parse(v)
                                for k, v in navigation.pop("$").items()}
                    else:
                        for a in list(navigation.keys()):
                            if a.startswith("$"):
                                v = navigation.pop(a)
                                args[a.strip("$")] = self._parse(v)

                if hasattr(attr, '__call__'):
                    result = attr(**args)
                else:
                    result = attr

                payload[key] = self._query(result, navigation)

            return payload

        raise TypeError("type %s is not supported" % type(x))

    def __call__(self, query, encode=False, **kw):
        if isinstance(query, str):
            query = json.loads(query)

        result = self._query(self, query)

        if encode:
            return json.dumps(result, **kw)

        return result
