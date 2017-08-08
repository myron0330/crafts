# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Attribute dict file
# **********************************************************************************#


class AttributeDict(dict):

    """
    A dict that allows direct attribute access to its keys.
    """

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__.__getitem__(item)
        elif item in self:
            return self.__getitem__(item)
        else:
            raise AttributeError("'dict' object has no attribute '{}'".format(item))

    def __setattr__(self, key, value):
        if key in self.__dict__:
            self.__dict__.__setitem__(key, value)
        elif key in self:
            self.__setitem__(key, value)
