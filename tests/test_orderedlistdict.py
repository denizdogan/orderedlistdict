from orderedlistdict import oldict
import json
import pytest


def items():
    return [
        ('foo', ['bar', 'baz']),
        ('1', [11, 111, 1111, 11111]),
        ('deep', [
            oldict([
                ('a', ['b', 'c'])
            ])
        ])
    ]


def pairs():
    ret = []
    for k, vs in items():
        for v in vs:
            ret.append((k, v))
    return ret


@pytest.fixture(scope = 'function')
def d():
    return oldict(items())


def test_add(d):

    # add new key with no values
    d.add('xyz')
    assert d['xyz'] == []

    # add new key with values
    d.add('abc', 'a', 'b', 'c')
    assert d['abc'] == ['a', 'b', 'c']

    # add values to existing key
    d.add('foo', 'qux')
    assert d['foo'] == ['bar', 'baz', 'qux']

    # add nothing to existing key
    d.add('foo')
    assert d['foo'] == ['bar', 'baz', 'qux']


def test_merge(d):
    e = oldict([

        # an existing key with new values
        ('foo', ['qux', 'lol']),

        # an existing key with no values
        ('deep', []),

        # a new key with new values
        ('blah', ['yada', 'bloop']),

        # a new key with no values
        ('xyz', []),

    ])

    d.merge(e)
    assert d['foo'] == ['bar', 'baz', 'qux', 'lol']
    assert len(d['deep']) == 1
    assert d['blah'] == ['yada', 'bloop']
    assert d['xyz'] == []


def test_from_pairs():

    # empty list of pairs
    old = oldict.from_pairs([])
    assert len(old) == 0

    # list of pairs with unique keys
    old = oldict.from_pairs([(1, 1), (2, 2)])
    assert len(old) == 2
    assert old[1] == [1]
    assert old[2] == [2]

    # list of pairs with non-unique keys
    old = oldict.from_pairs([(1, 1), (1, 11), (1, 111),
                             (2, 2), (2, 22), (2, 222)])
    assert old[1] == [1, 11, 111]
    assert old[2] == [2, 22, 222]


def test_copy(d):
    c = d.copy()
    assert c == d
    assert c is not d


def test_remove(d):

    # remove a single value, leaving one
    d.remove('foo', 'bar')
    assert d['foo'] == ['baz']

    # remove all values
    d.remove('1', 11, 111, 1111, 11111)
    assert '1' not in d

    # remove no values
    d.remove('deep')
    assert 'deep' in d


def test_items(d):
    assert d.items() == items()


def test_pairs(d):
    assert d.pairs() == pairs()


def test_json_dumps(d):
    assert json.dumps(d) == '{"foo": ["bar", "baz"], "1": [11, 111, 1111, 11111], "deep": [{"a": ["b", "c"]}]}'


def test_json_loads(d):
    assert json.loads(json.dumps(d), object_pairs_hook=oldict) == d


def test_repr(d):
    assert repr(d) == "OrderedListDict([('foo', ['bar', 'baz']), ('1', [11, 111, 1111, 11111]), ('deep', [OrderedListDict([('a', ['b', 'c'])])])])"


def test_dict_parity_equality(d):
    s = dict(items())

    # check that the oldict is equal to the dict
    assert d == s
