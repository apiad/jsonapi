# jsonapi

> A minimalistic JSON API framework in Python.

`jsonapi` is heavily inspired by [graphql](https://graphql.org), but aimed at a much simpler use case. The idea is to have a minimal framework for easily building JSON based APIs, that doesn't require any particular frontend technology. The design is inspired in `graphql`'s idea of a single fully customizable endpoint, but instead of defining a specific query language, `jsonapi` is entirely based on JSON both for the query and the response.

## Instalation

`jsonapi` is a single Python file with no dependencies that you can just clone and distribute with your project's source code:

    git clone https://github.com/apiad/jsonapi

## The basics

To illustrate the usage is best to start with an example. Let's begin with a simple API that exposes a single command, `ping`, which responds with the string `"pong"`. The main and only class in `jsonapi` is `JsonApi`, which defines all the available commands in the API as public methods:

```python
import jsonapi

class PingPong(JsonApi):
    def ping(self):
        return "pong"
```

Afterwards, create an instance of this API and call it's `query` method, passing along either a JSON-enconded string, or a pure Python dictionary:

```python
api = PingPong()

response = api.query({ "ping": True })
assert response == {
    "meta": {
        "errors": None
    },
    "payload": {
        "ping": "pong"
    }
}
```
