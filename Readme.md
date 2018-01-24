# jsonapi [![Travis](https://img.shields.io/travis/apiad/jsonapi.svg?style=flat-square)](https://travis-ci.org/apiad/jsonapi) [![Coveralls github](https://img.shields.io/coveralls/github/apiad/jsonapi.svg?style=flat-square)](https://coveralls.io/github/apiad/jsonapi?branch=master) [![GitHub tag](https://img.shields.io/github/tag/apiad/jsonapi.svg?style=flat-square&label=current%20version)](https://github.com/apiad/jsonapi/releases) ![Python versions](https://img.shields.io/badge/Python-3.4%2C%203.5%2C%203.6-blue.svg?style=flat-square)

> A minimalistic JSON API framework in Python with support for **graphql**-style queries.

**jsonapi** is heavily inspired by [graphql](https://graphql.org), but aimed at a much simpler use case. The idea is to have a minimal framework for easily building JSON based APIs, that doesn't require any particular frontend technology. The design is inspired in **graphql**'s idea of a single fully customizable endpoint, but instead of defining a specific query language, **jsonapi** is entirely based on JSON both for the query and the response, requires much less boilerplate code, only works in Python 3, and of course, is much less battle-tested. If you find **graphql** amazing but would like to try a decaffeinated version that you can setup in 10 lines, then give **jsonapi** a shot.

## Instalation

**jsonapi** is a single Python file with no dependencies that you can just clone and distribute with your project's source code:

    git clone https://github.com/apiad/jsonapi.git

## Hello world

To illustrate the usage is best to start with an example. The main class in **jsonapi** is (wait for it...) `JsonApi`, which defines all the available commands in the API as public methods:

```python
>>> from jsonapi import JsonApi

>>> class HelloWorld(JsonApi):
...     def say(self, message, args):
...         return message.format(args)

```

Afterwards, create an instance of this API and call it, passing along either a JSON-enconded string, or a pure Python dictionary, to query either methods or attributes:

```python
>>> api = HelloWorld()

>>> api({"say": { "$message": "Hello {0}!", "$args": "world" }})
{'say': 'Hello world!'}

```

## Moving on

There is more that can be done with **jsonapi**, read the [documentation](https://apiad.github.io/jsonapi/) to learn more:

* Perform [structured queries](https://apiad.github.io/jsonapi/#querying-complex-objects) with complex structure.
* Pass [arguments](https://apiad.github.io/jsonapi/operators#function-arguments) to commands.

## Contributing

Contributions are highly appreciated. Just fork and submit a pull request. All contributors will be granted credit on the following list:

* Alejandro Piad ([@apiad](https://github.com/apiad))

## Changelog

### In the roadmap

* Support for some meta commands (e.g., list's count)
* Support for operators ?? (e.g. exists, unsure about this)
* Support for method's arguments, including complex objects

### v0.1.2

* Suport for complex method arguments (parsed via `JsonObj`)

### v0.1.1

* Suport for plain method arguments

### v0.1

* Basic layout of the API
* Main features
  * Simple attribute and method based navigation
  * Automatic serialization to a JSON compatible object
* Basic documentation