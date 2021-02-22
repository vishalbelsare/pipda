from collections import OrderedDict

from pipda.verb import Verb
from pipda import *
from pipda.function import *

def test_function():

    @register_func
    def func(data, x):
        return data[x]

    ret = func([1], 0)
    assert ret == 1

    @register_verb
    def verb(data, x):
        return x

    ret = [2] >> verb(func(0))
    assert ret == 2

def test_function_deep():

    @register_func(context=Context.SELECT)
    def func(data, x):
        return {key: data[key] for key in x}

    @register_verb
    def verb(data, keys):
        return keys

    f = Symbolic()
    d = {'a': 1, 'b': 2, 'c': 3}
    ret = d >> verb(func([f.a, f.b]))
    assert ret == {'a': 1, 'b': 2}

    ret = d >> verb(func((f.a, f.b)))
    assert ret == {'a': 1, 'b': 2}

    ret = d >> verb(func({f.a, f.b}))
    assert ret == {'a': 1, 'b': 2}

    @register_func(context=Context.SELECT)
    def func_dict(data, x):
        return {key: data[key] for key in x.values()}

    ret = d >> verb(func_dict(OrderedDict([('x', f.a), ('y', f.b)])))
    assert ret == {'a': 1, 'b': 2}

    ret = d >> verb(func_dict({'x': f.a, 'y': f.b}))
    assert ret == {'a': 1, 'b': 2}

def test_function_called_in_normal_way():
    @register_func
    def func(data, x):
        return data[x]

    @register_verb
    def verb(data, x):
        return x

    r = [1, 2] >> verb(func(0) + 1)
    assert r == 2

    r = func(1, _force_piping=True).evaluate([0, 1])
    assert r == 1

