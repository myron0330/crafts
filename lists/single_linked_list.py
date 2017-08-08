# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Single linked list file
# **********************************************************************************#
from copy import copy


def recursive(formula, formatter=(lambda x: None)):
    def decorator(func):
        def _recursive(node, *args, **kwargs):
            if node.tail:
                return formula(_recursive(node.tail, *args, **kwargs), formatter(node))
            return func(node, *args, **kwargs)
        return _recursive
    return decorator


def traversal(func):
    def _traversal(node, *args, **kwargs):
        while node:
            func(node, *args, **kwargs)
            node = node.tail
    return _traversal


class Node(object):

    def __init__(self, obj, head=None, tail=None):
        self.head = head
        self.tail = tail
        self.obj = obj

    def append(self, node):
        self.tail = node
        node.head = self.tail


class SingleLinkedList(object):

    def __init__(self, link_head=None, link_tail=None):
        self.link_head = link_head
        self.link_tail = link_tail

    def __add__(self, other):
        assert isinstance(other, SingleLinkedList), 'Invalid item to add.'
        self.link_tail = self.link_head if self.link_tail is None else self.link_tail
        self.link_tail.tail = other.link_head
        self.link_tail = other.link_tail
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def append(self, node):
        if not self.link_head:
            self.link_head = self.link_tail = copy(node)
        else:
            self.link_tail.tail = self.link_tail = copy(node)

    def extend(self, nodes):
        for node in nodes:
            self.append(node)

    def recursive(self, formula, formatter):

        @recursive(formula, formatter)
        def executor(node):
            return formatter(node)

        return executor(self.link_head)

    def traversal(self, func, *args, **kwargs):

        @traversal
        def executor(node, *inner_args, **inner_kwargs):
            func(node, *inner_args, **inner_kwargs)

        return executor(self.link_head, *args, **kwargs)

    def get_length(self):
        return self.recursive(formula=(lambda x, y: x + y), formatter=(lambda x: 1))
