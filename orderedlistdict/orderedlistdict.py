from collections import defaultdict, OrderedDict


class OrderedListDict(defaultdict, OrderedDict):
    """
    A dictionary with list values where insertion order is retained.
    """

    def __init__(self, *args, **kwargs):
        OrderedDict.__init__(self, *args, **kwargs)
        defaultdict.__init__(self, list)

    def add(self, key, *values):
        """
        Add values to an entry.

        :param key: key of the entry
        :param values: values to add
        """
        self[key] += values

    def merge(self, other):
        """
        Merge with another dictionary.

        `other` can be any object which acts like a dict and which
        uses lists as values.

        :param other: dict-like object
        """
        for k, vs in other.iteritems():
            for v in vs:
                self[k].append(v)

    def remove(self, key, *values, **kwargs):
        """
        Remove values from an entry.

        If the entry has no values after removal, the entry itself
        will be deleted, unless keyword argument `keep` evaluates to
        :const:`True`.

        :param key: key of the entry
        :param values: values to remove
        :param kwargs: keyword arguments
        :raises KeyError: if `key` does not exist
        """
        if key not in self:
            raise KeyError(key)
        if not values:
            return
        self[key] = [ v for v in self[key] if v not in values ]
        keep = kwargs.get('keep')
        if not self[key] and not keep:
            del self[key]

    def pairs(self):
        """
        Return a list of key-value pairs
        """
        return list(self.iterpairs())

    def iterpairs(self):
        for k, vs in self.iteritems():
            for v in vs:
                yield (k, v)

    @classmethod
    def from_pairs(cls, iterable):
        ret = cls()
        for key, value in iterable:
            ret[key].append(value)
        return ret

    def copy(self):
        return self.__class__(self.iteritems())

    def __repr__(self):
        return 'OrderedListDict(%s)' % self.items()


# a shorter alias
oldict = OrderedListDict
