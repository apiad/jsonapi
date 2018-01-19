# coding: utf8

from jsonapi import JsonApi


class HelloWorld(JsonApi):
    def hello(self):
        return "world!"


def test_hello_world():
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


class MultipleCommands(JsonApi):
    def some_command(self):
        return "there you go"

    def some_other_command(self):
        return 42

    def and_yet_another(self):
        return True


def test_multiple_commands():
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
