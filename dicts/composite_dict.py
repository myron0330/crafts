# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Composite dict file
# **********************************************************************************#


class CompositeDict(dict):

    """
    A dict that allows to be used as a composite one without tedious initialization.
    """
    def __missing__(self, key):
        self.__setitem__(key, CompositeDict())
        return self.__getitem__(key)
