# coding: utf8

import json


class JsonObj:
    def _json(self, x, query):
        if isinstance(x, (int, float, str)):
            return x
        if isinstance(x, (list, tuple)):
            return [self._json(i, query) for i in x]
        if isinstance(x, dict):
            return { str(k): self._json(v) for k,v in x.items() }
        if isinstance(x, JsonObj):
            return x._query(query)
        raise TypeError("type %s is not supported" % type(x))

    def _query(self, query):
        if query is None:
            return {k: v for k, v in self.__dict__.items() if not hasattr(v, '__call__')}

        payload = {}

        if isinstance(query, dict):
            items = query.items()
        else:
            items = [(k, None) for k in query]

        for k,v in items:
            attr = getattr(self, k)
            args = {}
            navigation = v

            if hasattr(attr, '__call__'):
                result = attr(**args)
            else:
                result = attr

            payload[k] = self._json(result, navigation)

        return payload


class JsonApi(JsonObj):
    def __call__(self, query, encode=False):
        if isinstance(query, str):
            query = json.loads(query)

        result = self._query(query)

        if encode:
            return json.dumps(result)

        return result
