# jsonapi

> A minimalistic JSON API framework in Python with support for **graphql**-style queries.

**jsonapi** is heavily inspired by [graphql](https://graphql.org), but aimed at a much simpler use case. The idea is to have a minimal framework for easily building JSON based APIs, that doesn't require any particular frontend technology. The design is inspired in **graphql**'s idea of a single fully customizable endpoint, but instead of defining a specific query language, **jsonapi** is entirely based on JSON both for the query and the response, requires much less boilerplate code, only works in Python, and of course, is much less battle-tested. If you find **graphql** amazing but would like to try a decaffeinated version that you can setup in 10 lines, then give **jsonapi** a shoot.

## Instalation

**jsonapi** is a single Python file with no dependencies that you can just clone and distribute with your project's source code:

    git clone https://github.com/apiad/jsonapi.git

## Hello world

To illustrate the usage is best to start with an example. The main class in **jsonapi** is (wait for it...) `JsonApi`, which defines all the available commands in the API as public methods:

```python
>>> from jsonapi import JsonApi

>>> class HelloWorld(JsonApi):
...     def __init__(self):
...         self.the_answer = 42
...     def hello(self):
...         return "world!"

```

Afterwards, create an instance of this API and call it, passing along either a JSON-enconded string, or a pure Python dictionary, to query either methods or attributes:

```python
>>> api = HelloWorld()

>>> api({"hello"})
{'hello': 'world!'}

>>> api({"the_answer"})
{'the_answer': 42}

```

## Moving on

There is much more that can be done with **jsonapi**, read the [documentation](/docs/index.md) to learn more.

## Contributing

Contributions are highly appreciated. Just fork and submit a pull request. All contributors will be granted credit on the following list:

* Alejandro Piad ([@apiad](https://github.com/apiad))

## Changelog

### In the roadmap

* Support for method's arguments, including complex objects
* Support for some meta commands (e.g., list's count)
* Support for operators ?? (e.g. exists, unsure about this)

### v0.1

* Basic layout of the API
* Main features
  * Simple attribute and method based navigation
  * Automatic serialization to a JSON compatible object
* Basic documentation