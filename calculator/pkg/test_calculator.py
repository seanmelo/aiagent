def test_addition():
    assert 2 + 3 == 5


def test_subtraction():
    assert 5 - 2 == 3


def test_multiplication():
    assert 2 * 3 == 6


def test_division():
    assert 6 / 2 == 3


def test_operator_precedence():
    assert 2 + 3 * 4 == 14
    assert (2 + 3) * 4 == 20
