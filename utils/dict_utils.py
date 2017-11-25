# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Custom dict structures for doing interesting things.
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


class CompositeDict(dict):

    """
    A dict that allows to be used as a composite one without tedious initialization.
    """
    def __missing__(self, key):
        self.__setitem__(key, CompositeDict())
        return self.__getitem__(key)


class DefaultDict(dict):

    """
    A dict that allows set default value for any key(exist or in-exist).
    """
    def __init__(self, default=None):
        """
        Args:
            default(class or object): the specified default type or instance.
        """
        super(DefaultDict, self).__init__()
        self._default = default

    def __missing__(self, key):
        default = self._default() if isinstance(self._default, type) else self._default
        self.__setitem__(key, default)
        return self.__getitem__(key)


class OrderedDict(dict):

    """
    A dict that allows add or delete key-value object sequentially.
    """
    def __new__(cls, *args, **kwargs):
        cls.__orders__ = list()
        cls.__append__ = (lambda obj, item: obj.__orders__.append(item) if item not in obj.__orders__ else None)
        cls.__remove__ = \
            (lambda obj, item, default=None: obj.__orders__.remove(item) if item in obj.__orders__ else default)
        cls.__pop__ = \
            (lambda obj, item, default=0: obj.__orders__.pop(item) if item in range(len(obj.__orders__)) else default)
        cls.__inner_dict__ = dict()
        return super(OrderedDict, cls).__new__(OrderedDict, *args)

    def __setitem__(self, key, value):
        self.__append__(key)
        self.__inner_dict__.__setitem__(key, value)

    def __getitem__(self, item):
        return self.__inner_dict__.__getitem__(item)

    def __delitem__(self, key):
        self.__remove__(key)

    def __iter__(self):
        for key in self.__orders__:
            yield key

    def __add__(self, other):
        self.update(**other)
        return self

    def __radd__(self, other):
        self.__add__(other)
        return self

    def keys(self):
        """
        Returns:
            list: ordered keys.
        """
        return list(self.iterkeys())

    def values(self):
        """
        Returns:
            list: ordered values.
        """
        return list(self.itervalues())

    def items(self):
        """
        Returns:
            list: ordered items.
        """
        return list(self.iteritems())

    def itervalues(self):
        """
        Returns:
            iterable: ordered values iterator.
        """
        for key in self.__iter__():
            yield self.__inner_dict__.__getitem__(key)

    def iterkeys(self):
        """
        Returns:
            iterable: ordered keys iterator.
        """
        for key in self.__orders__:
            yield key

    def iteritems(self):
        """
        Returns:
            iterable: ordered items iterator.
        """
        for key in self.__orders__:
            yield (key, self.__inner_dict__.__getitem__(key))

    def setdefault(self, key, value=None):
        """
        Set default value for key if key doesn't exist, otherwise do nothing.

        Args:
            key(hashable): key
            value(object): optional. value, default is None.
        """
        if key not in self.__orders__:
            self.__append__(key)
            self.__inner_dict__.__setitem__(key, value)

    def pop(self, key, default=None):
        """
        Pop the key if key exist and return the corresponding value, otherwise return default.

        Args:
            key(hashable): key
            default(object): optional. default value, default is None.

        Returns:
            object: value corresponding to the key.
        """
        value = self.__getitem__(key) if key in self.__orders__ else default
        self.__remove__(key)
        return value

    def popitem(self):
        """
        Pop the first item from dict.

        Returns:
            tuple: key-value of the first item.
        """
        self.__pop__(0)
        return self.items()[0]

    def update(self, iterable=None, **dictionary):
        """
        Update dict from iterable and dictionary.
        If iterable present and has a .keys() method, does:     for k in iterable: dict[k] = iterable[k]
        If iterable present and lacks .keys() method, does:     for (k, v) in iterable: dict[k] = v
        In either case, this is followed by: for k in dictionary: dict[k] = dictionary[k]

        Args:
            iterable(iter): iterable instance, including list, dict, iterator etc.
            dictionary(dict): dict instance.
        """
        if iterable:
            if hasattr(iterable, 'keys'):
                for key, value in iterable.iteritems():
                    self.__setitem__(key, value)
            else:
                for key, value in iterable:
                    self.__setitem__(key, value)
        for key in dictionary:
            self.__setitem__(key, dictionary[key])

    def __repr__(self):
        return "{{{}}}".format(
            '\t'.join(map(str, self.items())).replace(',', ':').replace('(', '').replace(')', '').replace('\t', ', '))
