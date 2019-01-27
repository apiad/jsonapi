# jsonapi [![Travis](https://img.shields.io/travis/apiad/jsonapi.svg?style=flat-square)](https://travis-ci.org/apiad/jsonapi) [![Coveralls github](https://img.shields.io/coveralls/github/apiad/jsonapi.svg?style=flat-square)](https://coveralls.io/github/apiad/jsonapi?branch=master) ![Codacy grade](https://img.shields.io/codacy/grade/6cfc0cf3ee4b442bae0c43bf54a27a58.svg?style=flat-square) [![GitHub tag](https://img.shields.io/github/tag/apiad/jsonapi.svg?style=flat-square&label=current%20version)](https://github.com/apiad/jsonapi/releases) ![Python versions](https://img.shields.io/badge/Python-3.5%2C%203.6-blue.svg?style=flat-square)

> A minimalistic JSON API framework in Python with support for **graphql**-style queries.

**jsonapi** is heavily inspired by [graphql](https://graphql.org), but aimed at a much simpler use case. The idea is to have a minimal framework for easily building JSON based APIs, that doesn't require any particular frontend technology. The design is inspired in **graphql**'s idea of a single fully customizable endpoint, but instead of defining a specific query language, **jsonapi** is entirely based on JSON both for the query and the response, requires much less boilerplate code, only works in Python 3, and of course, is much less battle-tested. If you find **graphql** amazing but would like to try a decaffeinated version that you can setup in 10 lines, then give **jsonapi** a shot.

## Instalation

The easiest installation is through `pip`. Unfortunately the cute name `jsonapi` was taken already in PyPi, so the project is registered under `jsonapi-simple`.

```
pip install jsonapi-simple
```

You can also just clone and distribute with your project's source code:

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

* Perform [structured queries](https://apiad.github.io/jsonapi/quickstart#querying-complex-objects) with complex structure.
* Pass [arguments](https://apiad.github.io/jsonapi/operators#function-arguments) to commands.
* Obtain [aggregated data](https://apiad.github.io/jsonapi/operators#collection-operators) from collections.
* Manipulate [JSON data](https://apiad.github.io/jsonapi/jsonobj) with an object-oriented syntax.
* Get [type conversions](https://apiad.github.io/jsonapi/types) automatically for your API schema.

## Contributing

Contributions are highly appreciated. Just fork and submit a pull request. All contributors will be granted credit on the following list:

* Alejandro Piad ([@apiad](https://github.com/apiad))

## Changelog

### In the roadmap

* Automatic API documentation.

### v0.2.2

* Finally added to PyPi as [jsonapi-simple](https://pypi.org/project/jsonapi-simple/).

### v0.2.1

* Support for typed arguments.

### v0.2.0

* Support for meta operators in dictionaries (`_count`, `_items`, `_keys`, `_values`).
* The `JsonObj` constructor now receives either `str`, `dict` or a `**kwargs` mapping.

### v0.1.4

* Support for some meta operators for lists (`_count` and `_items`).

### v0.1.3

* Basic implementation of `JsonObj` for JSON manipulation.

### v0.1.2

* Suport for complex method arguments (parsed via `JsonObj`).

### v0.1.1

* Suport for plain method arguments.

### v0.1

* Basic layout of the API.
* Simple attribute and method based navigation.
* Automatic serialization to a JSON compatible object.
* Basic documentation.

## Issues and bugs

There are sure plenty of them. Just open an issue in Github.

## Colaboration

This project is licensed MIT, so you know the drill. Fork, open a pull request, and make sure to have up-to-date tests with (ideally) a 100% coverage.

For development purposes, make sure to have `pipenv` installed and run:

```
pipven install --dev
```

Then add your contributions, and make sure to run:

```
make test
```

Definitely you should pass all tests, and ideally also have 100% coverage. If that's case, open a pull request and I'm almost definitely will merge it.

## License

> MIT License
>
> Copyright (c) 2018 Alejandro Piad
>
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.
