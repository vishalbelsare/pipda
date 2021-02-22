from pipda.context import ContextEval, ContextSelect
import pytest
from pipda.symbolic import SubsetRef
from pipda import *

def test_symbolic():
    f = Symbolic()
    assert isinstance(f.a, SubsetRef)
    assert isinstance(f['a'], SubsetRef)
    assert f.evaluate(1) == 1

def test_subsetref():
    f = Symbolic()
    assert f.a.evaluate(1, ContextSelect()) == 'a'
    assert f['a'].evaluate(1, ContextSelect()) == 'a'
    assert f['a'].evaluate({'a': 2}, ContextEval()) == 2
    assert isinstance(f.a.evaluate(1, None), SubsetRef)
    with pytest.raises(NotImplementedError):
        f.a.a
    with pytest.raises(NotImplementedError):
        f.a['a']
    # expr = f['a']['a']
    # assert expr.evaluate({'a': {'a': 2}}) == 2

    # with pytest.raises(TypeError):
    assert f[1].evaluate(0, ContextSelect()) == 1
