---
layout: default
---
# jsonapi

**jsonapi** is heavily inspired by [graphql](https://graphql.org), but aimed at a much simpler use case. The idea is to have a minimal framework for easily building JSON based APIs, that doesn't require any particular frontend technology. The design is inspired in **graphql**'s idea of a single fully customizable endpoint, but instead of defining a specific query language, **jsonapi** is entirely based on JSON both for the query and the response, requires much less boilerplate code, only works in Python, and of course, is much less battle-tested. If you find **graphql** amazing but would like to try a decaffeinated version that you can setup in 10 lines, then give **jsonapi** a shot.

## Installation

**jsonapi** is a single Python file with no dependencies that you can just clone and distribute with your project's source code:

    git clone https://github.com/apiad/jsonapi.git

## Hello world

To illustrate the usage is best to start with an example. The main class in **jsonapi** is (wait for it...) `JsonApi`, which defines all the available commands in the API as public methods:

```python
>>> from jsonapi import JsonApi
>>> from pprint import pprint

>>> class HelloWorld(JsonApi):
...     def hello(self):
...         return "world!"
...     def the_answer(self):
...         return 42

```

Afterwards, create an instance of this API and call it, passing along either a JSON-enconded string, or a pure Python dictionary:

```python
>>> api = HelloWorld()

>>> api({"hello"})
{'hello': 'world!'}

>>> api({"the_answer"})
{'the_answer': 42}

```

The way to invoke a particular command is to add it in the query JSON body, much like in **graphql**. The cool part is when we have several commands. Usually we would set up different endpoints, with a method registered for each different command. In **jsonapi** you simply write different methods, and set up a single endpoint. Then on the query, you decide which command to execute (which method to call):

```python
>>> response = api({"hello", "the_answer"})
>>> pprint(response)
{'hello': 'world!', 'the_answer': 42}

```

## Querying complex objects

The coolest part of **jsonapi** is how you can extend an API with commands that return full featured classes, which expose commands themselves. This way you can create a complex structure and let the query describe exactly what to get. First let's define a slightly more complex API. Here we are simulating a small database:

```python
>>> from jsonapi import JsonApi, JsonObj

>>> class StarWars(JsonApi):
...     def characters(self):
...         return [luke, leia, han]

>>> class Character(JsonObj):
...     def __init__(self, name, lastname):
...         self.name = name
...         self.lastname = lastname
...
...     def fullname(self):
...         return "%s %s" % (self.name, self.lastname)
...
...     def friends(self):
...         return FRIENDS[self]

>>> luke = Character(name="Luke", lastname="Skywalker")
>>> leia = Character(name="Leia", lastname="Skywalker")
>>> han = Character(name="Han", lastname="Solo")

>>> FRIENDS = {
...     luke: [han, leia],
...     leia: [luke],
...     han: [luke],
... }

```

Now we can query this API as usual:

```python
>>> api = StarWars()

>>> response = api({ 'characters' })
>>> pprint(response)
{'characters': [{'lastname': 'Skywalker', 'name': 'Luke'},
                {'lastname': 'Skywalker', 'name': 'Leia'},
                {'lastname': 'Solo', 'name': 'Han'}]}

```

By default, we'll receive as response the JSON representation of the objects, built out of their attributes (only those which are JSON serializable, of course). This magic is done by the `JsonObj` class, so make sure to always inherit this class for the types you want to expose in the API.

However, we can also build more complex queries, that allow us to shape the response. For instance, we can query for a specific attribute (or method):

```python
>>> response = api({
...     'characters': {
...         'fullname'
...     }
... })
>>> pprint(response)
{'characters': [{'fullname': 'Luke Skywalker'},
                {'fullname': 'Leia Skywalker'},
                {'fullname': 'Han Solo'}]}

```

And of course, this can be applied recursively *ad infinitum*:

```python
>>> response = api({
...     'characters': {
...         'name': None,
...         'friends': { 'name' }
...     }
... })
>>> pprint(response)
{'characters': [{'friends': [{'name': 'Han'}, {'name': 'Leia'}],
                 'name': 'Luke'},
                {'friends': [{'name': 'Luke'}], 'name': 'Leia'},
                {'friends': [{'name': 'Luke'}], 'name': 'Han'}]}

```

**NOTE** that we had to write `"name": None`, otherwise it wouldn't have been a valid Python expression, since we'd be mixing set syntax and dictionary syntax in the same key. Sadly, in pure JSON we don't have sets, so we'll have toset the value `null` to the keys which have no sub-queries.

## Moving on

Keep reading about [operators](/operators.md).

<script
  src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
  integrity="sha256-3edrmyuQ0w65f8gfBsqowzjJe2iM6n0nKciPUp8y+7E="
  crossorigin="anonymous"></script>
<script src="/jsonapi/assets/js/demo.js"></script>
