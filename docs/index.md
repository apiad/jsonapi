---
layout: default
---

# jsonapi

> A minimalistic JSON API framework in Python with support for **graphql**-style queries.

**jsonapi** is heavily inspired by [graphql](https://graphql.org), but aimed at a much simpler use case. The idea is to have a minimal framework for easily building JSON based APIs, that doesn't require any particular frontend technology. The design is inspired in **graphql**'s idea of a single fully customizable endpoint, but instead of defining a specific query language, **jsonapi** is entirely based on JSON both for the query and the response, requires much less boilerplate code, only works in Python, and of course, is much less battle-tested. If you find **graphql** amazing but would like to try a decaffeinated version that you can setup in 10 lines, then give **jsonapi** a shoot.

## Instalation

**jsonapi** is a single Python file with no dependencies that you can just clone and distribute with your project's source code:

    git clone https://github.com/apiad/jsonapi.git

## The basics

To illustrate the usage is best to start with an example. The main class in **jsonapi** is (wait for it...) `JsonApi`, which defines all the available commands in the API as public methods:

```python
from jsonapi import JsonApi

class HelloWorld(JsonApi):
    def hello(self):
        return "world!"

    def the_answer(self):
        return 42
```

Afterwards, create an instance of this API and call it's `query` method, passing along either a JSON-enconded string, or a pure Python dictionary:

```python
api = HelloWorld()

response = api({"hello": None})
expected = {
    "hello": "world!"
}
assert response == expected
```

The way to invoke a particular command is to add it in the query JSON body, much like in **graphql**. Since we are dealing with standard JSON, we need to add that `None` value (or `null` is actual JSON), because they key cannot appear by itself. The cool part is when we have several commands. Usually we would set up different endpoints, with a method registered for each different command. In **jsonapi** you simply write different methods, and set up a single endpoint.

```python
response = api({"hello": None, "the_answer": None})
expected = {
    "hello": "world!",
    "the_answer": 42
}
assert response == expected
```

The coolest part of **jsonapi** is how you can extend an API with commands that return full featured classes, which expose commands themselves. This way you can create a complex structure and let the query describe exactly what to get. First let's define a slightly more complex API. Here we are simulating a small database:

```python
from jsonapi import JsonApi, JsonObj

class StarWars(JsonApi):
    def characters(self):
        return [luke, leia, han]

class Character(JsonObj):
    def __init__(self, name, lastname):
        self.name = name
        self.lastname = lastname

    def fullname(self):
        return self.name + self.lastname

    def friends(self):
        return FRIENDS[self]

luke = Character(name="Luke", lastname="Skywalker")
leia = Character(name="Leia", lastname="Skywalker")
han = Character(name="Han", lastname="Solo")

FRIENDS = {
    luke: [han, leia],
    leia: [luke],
    han: [luke],
}
```

Now we can query this API as usual:

```python
api = StarWars()

response = api({ 'characters': None })
expected = {
    'characters': [
        {'name': 'Luke', 'lastname': 'Skywalker' },
        {'name': 'Leia', 'lastname': 'Skywalker' },
        {'name': 'Han', 'lastname': 'Solo' },
    ]
}
assert response == expected
```

By default, we'll receive as response the JSON representation of the objects, built out of their attributes (only those which are JSON serializable, of course). This magic is done by the `JsonObj` class, so make sure to always inherit this class for the types you want to expose in the API.

However, we can also build more complex queries, that allow us to shape the response. For instance, we can query for a specific attribute or method:

```python
response = api.query({
    'characters': {
        'fullname': None
    }
})
expected = {
    'characters': [
        {'fullname': 'Luke Skywalker' },
        {'fullname': 'Leia Skywalker' },
        {'fullname': 'Han Solo' },
    ]
}
assert response == expected
```