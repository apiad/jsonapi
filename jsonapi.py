# coding: utf8

import json


class JsonObj:
    def __init__(self, data=None, **kwargs):
        if isinstance(data, str):
            data = json.loads(data)

        if isinstance(data, dict):
            data.update(**kwargs)
        else:
            data = kwargs

        for k,w in data.items():
            setattr(self, str(k), self._parse(w))

    def dict(self):
        return {
            key: self._json(value) for key, value
                 in self.__dict__.items()
                 if not hasattr(value, '__call__')
        }

    def json(self, **kwargs):
        return json.dumps(self.dict(), **kwargs)

    def _json(self, x):
        if x is None:
            return None
        if isinstance(x, (int, float, str, bool)):
            return x
        if isinstance(x, (list, tuple, set)):
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
        if isinstance(x, (list, tuple, set)):
            return [self._parse(i) for i in x]
        if isinstance(x, dict):
            return JsonObj(**x)

        raise TypeError("type %s is not supported" % type(x))

    def __repr__(self):
        return "JsonObj(%s)" % str(self.dict())


class JsonApi(JsonObj):
    def _query(self, obj, query):
        if obj is None:
            return None
        if isinstance(obj, (int, float, str, bool)):
            return obj
        if isinstance(obj, dict):
            return {str(k): self._query(v, query) for k, v in obj.items()}
        if hasattr(obj, '__iter__'):
            return self._query_iter(obj, query)
        if isinstance(obj, JsonObj):
            return self._query_obj(obj, query)

        raise TypeError("type %s is not supported" % type(obj))

    def _query_iter(self, obj, query):
        meta, query = self._extract(query, '_')

        if not meta:
            return [self._query(i, query) for i in obj]

        result = {}

        for m,v in meta.items():
            result["_%s" % m] = getattr(self, '_meta_%s' % m)(obj, v)

        return result

    def _query_obj(self, obj, query):
        if not query:
            return obj.dict()

        payload = {}

        for key, value in query.items():
            attr = getattr(obj, key)
            args, query = self._extract(value, "$", True)

            if hasattr(attr, '__call__'): result = attr(**args)
            else: result = attr

            payload[key] = self._query(result, query)

        return payload

    def _extract(self, query, label, parse=False):
        if not query:
            return {}, query

        if label in query:
            return query.pop(label), query

        args = {}

        for a in list(query):
            if a.startswith(label):
                v = query.pop(a)
                if parse:
                    v = self._parse(v)
                args[a.strip(label)] = v

        return args, query

    @staticmethod
    def _meta_count(obj, query):
        return len(obj)

    def _meta_items(self, obj, query):
        return [self._query(i, query) for i in obj]

    def _parse_query(self, query):
        if query is None:
            return {}
        if isinstance(query, (int, float, str, bool)):
            return query
        if isinstance(query, (list, tuple, set)):
            return { str(i): None for i in query }
        if isinstance(query, dict):
            return { str(k): self._parse_query(v) for k,v in query.items() }

        raise TypeError("type %s is not supported" % type(query))

    def __call__(self, query, encode=False, **kw):
        if isinstance(query, str):
            query = json.loads(query)

        query = self._parse_query(query)
        result = self._query(self, query)

        if encode:
            return json.dumps(result, **kw)

        return result
