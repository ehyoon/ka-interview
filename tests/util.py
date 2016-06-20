def verify_arrays_have_same_content(res, expected):
    _expected = set(expected)
    assert len(res) == len(expected)
    for el in res:
        if el in _expected:
            _expected.remove(el)
        else:
            assert False
    assert len(_expected) == 0