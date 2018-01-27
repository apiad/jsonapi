---
layout: default
---

# Operators

When specifying a query, you have the option not only to declare the expected output structure, but also to specify input arguments and apply some query operators.

## Function arguments

The next thing you'll probably want is to pass some arguments to your functions. There are two ways to do this in **jsonapi**. The cannonical way is to add a key `"$"` with a dictionary of argument values:

```python
>>> from jsonapi import JsonApi, JsonObj

>>> class Calculator(JsonApi):
...     def sum(self, a, b):
...         return a + b
...     def mult(self, a, b=1):
...         return a * b

>>> api = Calculator()
>>> api({ "sum": { "$": { "a": 27, "b": 15 } } })
{'sum': 42}

```

You can also use the "lazy" way, which is simply to prepend `"$"` to all arguments:

```python
>>> api({ "sum": { "$a": 27, "$b": 15 } })
{'sum': 42}

```

Default arguments are, of course, default:

```python
>>> api({ "mult": { "$a": 42 } })
{'mult': 42}

```

## Complex function arguments

If your function receives a complex argument (i.e., a JSON dict), you will automatically receive a parsed `JsonObj` that you can manipulate with dot-notation access for attributes:

```python
>>> class ComplexArg(JsonApi):
...     def process(self, x):
...         return x.message.format(x.name)

>>> api = ComplexArg()
>>> api({ 'process': { '$x': { 'name': 'world', 'message': 'Hello {0}!'} }})
{'process': 'Hello world!'}

```

You can read more about `JsonObj`'s magic tricks [here](/jsonobj.md).

## Collection operators

For collections we have a couple interesting operators that return some aggregated information about the collection itself. These operators are used the same way as standard navigation, but their names start with `_`. In turn, these operators are not applied on the collection's content, but instead on the collection itself.

The `_count` operator returns the number of items in the collection:

```python
>>> class CountApi(JsonApi):
...     def elements(self):
...         return list(range(10))

>>> api = CountApi()
>>> api({ 'elements' })
{'elements': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}

>>> api({ 'elements': { '_count' }})
{'elements': {'_count': 10}}

```

Now the problem is that you lost the items themselves. Well, this can fixed by calling another operator `_items` which returns back the items of the collection:

```python
>>> from pprint import pprint

>>> r = api({ 'elements': { '_count', '_items' }})
>>> pprint(r)
{'elements': {'_count': 10, '_items': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}}

```

If you need to define a sub-query on the items, and still need the count, you can add the query specification to the `_items` operator:

```python
>>> class ItemsApi(JsonApi):
...     def elements(self):
...         return [JsonObj(value=i, square=i*i) for i in range(5)]

>>> api = ItemsApi()

>>> r = api({ 'elements': { '_count': None, '_items': { 'square' } }})
>>> pprint(r)
{'elements': {'_count': 5,
              '_items': [{'square': 0},
                         {'square': 1},
                         {'square': 4},
                         {'square': 9},
                         {'square': 16}]}}

```

Both of these operators also works with dictionary-like objects:

```python
>>> class DictApi(JsonApi):
...     def elements(self):
...         return {i: dict(square=i*i, cube=i*i*i) for i in range(5)}

>>> api = DictApi()

>>> r = api({ 'elements': { '_count': None, '_items': { 'square' } }})
>>> pprint(r)
{'elements': {'_count': 5,
              '_items': {'0': {'square': 0},
                         '1': {'square': 1},
                         '2': {'square': 4},
                         '3': {'square': 9},
                         '4': {'square': 16}}}}

```

**NOTE** that using the `_items` operator on a `dict` is the only way to apply a
sub-query on the values of the dictionary. If you wanted to do the previous query without
`_items` this is what you would get an exception saying that there is no `square` key in
the dictionary, and it's true, because the dictionary keys are `0`, `1`, etc.

```python
>>> try:
...     r = api({ 'elements': { 'square' } })
... except AttributeError as e:
...     e
AttributeError("'JsonObj' object has no attribute 'square'",)

```

You can also directly query for `_keys` and `_values` (using sub-queries to select inside the values):

```python
>>> r = api({'elements': { '_keys': None, '_values': {'cube'} }})
>>> pprint(r)
{'elements': {'_keys': [0, 1, 2, 3, 4],
              '_values': [{'cube': 0},
                          {'cube': 1},
                          {'cube': 8},
                          {'cube': 27},
                          {'cube': 64}]}}

```