# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Dicts test file
# **********************************************************************************#
import unittest
from nose_parameterized import param, parameterized
from ... basic import DefaultDict, CompositeDict, OrderedDict, AttributeDict


class TestDefaultDict(unittest.TestCase):

    @parameterized.expand(
        [
            param(set, (lambda x: x.add(1))),
            param(list, (lambda x: x.append(1))),
            param(dict, (lambda x: x.update({'key': 1})))
        ]
    )
    def test_default_dict(self, default, operate):
        obj = DefaultDict(default)
        operate(obj['test'])
        print obj


class TestCompositeDict(unittest.TestCase):

    def test_composite_dict(self):
        obj = CompositeDict()
        obj['this']['is']['a']['fantastic']['dict'] = True
        print obj


class TestOrderedDict(unittest.TestCase):

    def test_ordered_dict(self):
        obj = OrderedDict()
        for key in xrange(5):
            obj['test{}'.format(key)] = key
        print 'Obj: ', obj
        print 'Keys: ', obj.keys()
        print 'Values: ', obj.values()
        print 'Items before popitem: ', obj.items()
        obj.popitem()
        print 'Items after popitem: ', obj.items()
        obj.pop('test3')
        print 'Obj: ', obj
        print 'Keys: ', obj.keys()
        print 'Values: ', obj.values()
        obj += {'added': 'item'}
        print 'Obj: ', obj


class TestAttributeDict(unittest.TestCase):

    def test_attribute_dict(self):
        obj = AttributeDict()
        obj['fantasy'] = 1
        print obj['fantasy'], obj.fantasy
