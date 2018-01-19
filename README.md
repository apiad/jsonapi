# jsonapi

> A minimalistic JSON API framework in Python.

**jsonapi** is heavily inspired by [graphql](https://graphql.org), but aimed at a much simpler use case. The idea is to have a minimal framework for easily building JSON based APIs, that doesn't require any particular frontend technology. The design is inspired in **graphql**'s idea of a single fully customizable endpoint, but instead of defining a specific query language, **jsonapi** is entirely based on JSON both for the query and the response.

## Instalation

**jsonapi** is a single Python file with no dependencies that you can just clone and distribute with your project's source code:

    git clone https://github.com/apiad/jsonapi.git

## The basics

To illustrate the usage is best to start with an example. The main and only class in **jsonapi** is (wait for it...) `JsonApi`, which defines all the available commands in the API as public methods:

```python
from jsonapi import JsonApi

class HelloWorld(JsonApi):
    def hello(self):
        return "world!"
```

Afterwards, create an instance of this API and call it's `query` method, passing along either a JSON-enconded string, or a pure Python dictionary:

```python
api = HelloWorld()

response = api.query({"hello": None})
expected = {
    "meta": {
        "error": None
    },
    "payload": {
        "hello": "world!"
    }
}
assert response == expected
```

The way to invoke a particular command is to add it in the query JSON body, much like in **graphql**. Since we are dealing with standard JSON, we need to add that `None` value (or `null` is actual JSON), because they key cannot appear by itself. The cool part is when we have several commands. Usually we would set up different endpoints, with a method registered for each different command. In **jsonapi** you simply write different methods, and set up a single endpoint:

```python
class MultipleCommands(JsonApi):
    def some_command(self):
        return "there you go"

    def some_other_command(self):
        return 42

    def and_yet_another(self):
        return True
```

The query in itself defines what to call:

```python
api = MultipleCommands()

response = api.query({"some_command": None})
expected = {
    "meta": {
        "error": None
    },
    "payload": {
        "some_command": "there you go"
    }
}
assert response == expected
```

You can even query for several commands at once:

```python
response = api.query({"some_other_command": None, "and_yet_another": None})
expected = {
    "meta": {
        "error": None
    },
    "payload": {
        "some_other_command": 42,
        "and_yet_another": True
    }
}
assert response == expected
```