# coding: utf-8

__all__ = ['JsonObj', 'JsonApi', 'parse']

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
            setattr(self, str(k), parse(w))

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

    def __repr__(self):
        return "JsonObj(%s)" % str(self.dict())


def parse(x):
    if x is None:
        return None
    if isinstance(x, (int, float, str, bool)):
        return x
    if isinstance(x, (list, tuple, set)):
        return [parse(i) for i in x]
    if isinstance(x, dict):
        return JsonObj(x)

    raise TypeError("type %s is not supported" % type(x))


class JsonApi(JsonObj):
    def __call__(self, query, encode=False, **kw):
        if isinstance(query, str):
            query = json.loads(query)

        query = _parse_query(query)
        result = _query(self, query)

        if encode:
            return json.dumps(result, **kw)

        return result


def _query(obj, query):
    if obj is None:
        return None
    if isinstance(obj, (int, float, str, bool)):
        return obj
    if isinstance(obj, dict):
        return _query_dict(obj, query)
    if hasattr(obj, '__iter__'):
        return _query_iter(obj, query)
    if isinstance(obj, JsonObj):
        return _query_obj(obj, query)

    raise TypeError("type %s is not supported" % type(obj))


def _query_iter(obj, query):
    meta, query = _extract(query, '_')

    if not meta:
        return [_query(i, query) for i in obj]

    result = {}

    for m, v in meta.items():
        result["_%s" % m] = globals()['_meta_%s' % m](obj, v)

    return result


def _query_dict(obj, query):
    meta, query = _extract(query, '_')

    if not meta:
        return _query_obj(JsonObj(obj), query)

    result = {}

    for m, v in meta.items():
        result["_%s" % m] = globals()['_meta_%s' % m](obj, v)

    return result


def _query_obj(obj, query):
    if not query:
        return obj.dict()

    payload = {}

    for key, value in query.items():
        attr = getattr(obj, key)
        args, query = _extract(value, "$", True)

        if hasattr(attr, '__call__'):
            if attr.__annotations__:
                args = _convert(args, attr.__annotations__)
            result = attr(**args)
        else:
            result = attr

        payload[key] = _query(result, query)

    return payload


def _extract(query, label, parse_obj=False):
    if not query:
        return {}, query

    if label in query:
        return query.pop(label), query

    args = {}

    for a in list(query):
        if a.startswith(label):
            v = query.pop(a)
            if parse_obj:
                v = parse(v)
            args[a.strip(label)] = v

    return args, query


def _convert(args, annotations):
    result = {}

    for k, v in args.items():
        if k in annotations:
            result[k] = annotations[k](**v.dict())
        else:
            result[k] = v

    return result


def _meta_count(obj, query):
    return len(obj)


def _meta_items(obj, query):
    if isinstance(obj, list):
        return [_query(i, query) for i in obj]
    if isinstance(obj, dict):
        return {str(k): _query(v, query) for k, v in obj.items()}


def _meta_keys(obj, query):
    return list(obj.keys())


def _meta_values(obj, query):
    return [_query(v, query) for v in obj.values()]


def _parse_query(query):
    if query is None:
        return {}
    if isinstance(query, (int, float, str, bool)):
        return query
    if isinstance(query, (list, tuple, set)):
        return {str(i): None for i in query}
    if isinstance(query, dict):
        return {str(k): _parse_query(v) for k, v in query.items()}

    raise TypeError("type %s is not supported" % type(query))
