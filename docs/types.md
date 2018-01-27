---
layout: default
---

# Adding type annotations

If you add type annotations to your method arguments, `JsonApi` will parse them accordingly before
passing them to corresponding methods. The easiest way to use this feature is to declare your own
classes inheriting from `JsonObj`, so you get a free out-of-the-box dictionary to object constructor.
Make sure to **always** initialize like it's shown below, passing the corresponding `**kwargs` to `JsonApi`:

```python
>>> from pprint import pprint
>>> from jsonapi import JsonApi, JsonObj

>>> class Person(JsonObj):
...     def __init__(self, first_name, last_name):
...         super(Person, self).__init__(first_name=first_name, last_name=last_name)
...
...     def fullname(self):
...        return "%s %s" % (self.first_name, self.last_name)

>>> class PersonApi(JsonApi):
...     def name_it(self, person: Person):
...         return person.fullname()

>>> api = PersonApi()
>>> r = api({ 'name_it': {'$person': {'first_name': 'John',
...                                   'last_name': 'Doe' }}})
>>> pprint(r)
{'name_it': 'John Doe'}

```
