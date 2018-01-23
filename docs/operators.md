---
layout: default
---

# Operators

The next thing you'll probably want is to pass some arguments to your functions. There are two ways to do this in **jsonapi**. The cannonical way is to add a key `"$"` with a dictionary of argument values:

```python
>>> from jsonapi import JsonApi

>>> class Calculator(JsonApi):
...     def sum(self, a, b):
...         return a + b
...     def mult(self, a, b=1):
...         return a * b

>>> api = Calculator()
>>> api({ "sum": { "$": { "a": 27, "b": 15 } } })
{'sum': 42}

```

You can also use the  "lazy" way, which is simply to prepend `"$"` to all arguments:

```python
>>> api({ "sum": { "$a": 27, "$b": 15 } })
{'sum': 42}

```

Default arguments are, of course, default:

```python
>>> api({ "mult": { "$a": 42 } })
{'mult': 42}

```
