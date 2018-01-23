---
layout: default
---

# Operators

When specifying a query, you have the option not only to declare the expected output structure, but also to specify input arguments and apply some query operators.

## Function arguments

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