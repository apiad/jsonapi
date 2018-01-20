# coding: utf8

from jsonapi import JsonApi, JsonObj


class HelloWorld(JsonApi):
    def hello(self):
        return "world!"


def test_hello_world():
    api = HelloWorld()

    response = api({"hello": None})
    expected = {
        "hello": "world!"
    }
    assert response == expected


class MultipleCommands(JsonApi):
    def some_command(self):
        return "there you go"

    def some_other_command(self):
        return 42

    def and_yet_another(self):
        return True


def test_multiple_commands():
    api = MultipleCommands()

    response = api({"some_command": None})
    expected = {
        "some_command": "there you go"
    }
    assert response == expected

    response = api({"some_other_command": None, "and_yet_another": None})
    expected = {
        "some_other_command": 42,
        "and_yet_another": True
    }
    assert response == expected


class StarWars(JsonApi):
    def characters(self):
        return [luke, leia, han]


class Character(JsonObj):
    def __init__(self, name, lastname):
        self.name = name
        self.lastname = lastname

    def fullname(self):
        return self.name + " " + self.lastname

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


def test_jsonobj():
    api = StarWars()

    response = api({
        'characters': None
    })
    expected = {
        'characters': [
            {'name': 'Luke', 'lastname': 'Skywalker'},
            {'name': 'Leia', 'lastname': 'Skywalker'},
            {'name': 'Han', 'lastname': 'Solo'},
        ]
    }
    assert response == expected


def test_call_method():
    api = StarWars()

    response = api({
        'characters': {
            'fullname': None
        }
    })
    expected = {
        'characters': [
            {'fullname': 'Luke Skywalker'},
            {'fullname': 'Leia Skywalker'},
            {'fullname': 'Han Solo'},
        ]
    }
    assert response == expected
