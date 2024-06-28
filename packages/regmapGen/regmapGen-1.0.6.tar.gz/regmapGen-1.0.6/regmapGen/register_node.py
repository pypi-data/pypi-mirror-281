#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Functions for XLS Parser
"""


class RegisterNode(object):
    def __init__(self, name='root'):
        self.name = name
        self.items = {}
        self.attrs = {}

    def __iter__(self):
        return iter(self.items.items())

    def __setitem__(self, key, value):
        self.items[key] = value

    def __getitem__(self, key):
        return self.items[key]

    def __setattr__(self, key, value):
        if key in ['name', 'items', 'attrs']:
            super().__setattr__(key, value)
        else:
            self.attrs[key] = value

    def __getattr__(self, key):
        if key in self.attrs:
            return self.attrs[key]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")

    def __delattr__(self, key):
        if key in self.attrs:
            del self.attrs[key]
        else:
            super().__delattr__(key)

    def __delitem__(self, key):
        del self.items[key]

    def keys(self):
        return self.items.keys()

    def iter_items(self):
        return self.items.items()
