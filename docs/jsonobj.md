---
layout: default
---

# JSON manipulation

`JsonObj` is the swiss-army knife for JSON manipulation. It bridges the world of object oriented programming with the JSON representation. You can use a `JsonObj` instance as a regular Python object, setting attribute values, and then obtain a JSON representation easily (you can pass to the `json` method the same args as to the `json.dumps` method):

```python
>>> from jsonapi import JsonObj
>>> obj = JsonObj()
>>> obj.x = 5
>>> obj.y = JsonObj()
>>> obj.y.z = [1,{2:3},None]
>>> obj.json(sort_keys=True)
'{"x": 5, "y": {"z": [1, {"2": 3}, null]}}'

```

The way this works is actually because `JsonObj` can be converted directly to a dictionary represenation, which can be later serialized as JSON (notice how keys are converted to their `str` representation automatically):

```python
>>> from pprint import pprint
>>> pprint(obj.dict())
{'x': 5, 'y': {'z': [1, {'2': 3}, None]}}

```

The opposite also works, i.e., you can create a `JsonObj` from a dictionary and use it with dot-notation for attribute access:

```python
>>> d = {'x': 5, 'y': {'z': [1, {'2': 3}, None]}}
>>> obj = JsonObj(d)
>>> obj.y.z[1].dict()
{'2': 3}

```

You can also very easily load a JSON file and use it as an object:

```python
>>> s = '{"x": 5, "y": {"z": [1, {"2": 3}, null]}}'
>>> obj = JsonObj(s)
>>> obj.y.z[1].dict()
{'2': 3}

```
