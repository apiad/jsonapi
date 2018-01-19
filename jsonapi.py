# coding: utf8

import json


class JsonApi:
    def _query(self, data):
        payload = {}

        for k,v in data.items():
            method = getattr(self, k)

            if v is None:
                payload[k] = method()
            else:
                payload[k] = method(v)

        return payload

    def query(self, data, encode=False):
        if isinstance(data, str):
            data = json.loads(data)

        try:
            result = dict(
                meta=dict(error=None),
                payload=self._query(data),
            )
        except Exception as e:
            result = dict(
                meta=dict(error=str(e)),
                payload=None,
            )

        if encode:
            return json.dumps(result)

        return result
