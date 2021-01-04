
import pytest
parametrize = pytest.mark.parametrize

from riptable import *


SYMBOLS = ['AAPL', 'AMZN', 'FB', 'GOOG', 'IBM']
NB_PARALLEL_SYMBOLS = SYMBOLS * 2000
assert len(NB_PARALLEL_SYMBOLS) >= FAString._APPLY_PARALLEL_THRESHOLD


class TestStr:

    cat_symbol = Cat(np.tile(np.arange(len(SYMBOLS) + 1), 3), SYMBOLS)

    def test_cat(self):
        arrsize = 200
        symbol = Cat(1 + arange(arrsize) % len(SYMBOLS), SYMBOLS)
        result = symbol.expand_array.str.startswith('AAPL') == symbol.str.startswith(
            'AAPL'
        )
        assert np.all(result)

    def test_cat_filtered(self):
        result = self.cat_symbol.expand_array.str.startswith('IBM') == self.cat_symbol.str.startswith(
            'IBM'
        )
        assert np.all(result)

    def test_lower(self):
        result = FAString(SYMBOLS).lower
        assert (result.tolist() == [s.lower() for s in SYMBOLS])

    def test_lower_cat(self):
        result = self.cat_symbol.str.lower
        expected = Cat(self.cat_symbol.ikey, [s.lower() for s in SYMBOLS])
        assert (result == expected).all()

    def test_upper(self):
        result = FAString(SYMBOLS).upper
        assert (result.tolist() == [s.upper() for s in SYMBOLS])

    def test_upper_cat(self):
        result = self.cat_symbol.str.upper
        expected = Cat(self.cat_symbol.ikey, [s.upper() for s in SYMBOLS])
        assert (result == expected).all()

    @parametrize("str2, expected", [
        ('bb', [False, False, True]),
        ('ba', [False, True, False]),
    ])
    def test_endswith(self, str2, expected):
        result = FAString(['abab', 'ababa', 'abababb']).endswith(str2)
        assert np.array_equal(result, expected)

    @parametrize("str2, expected", [
        ('A', [True, True, False, False, False]),
        ('AA', [True, False, False, False, False]),
        ('', [True] * 5),
        ('AAA', [False] * 5),
        ('AAPL', [True] + [False] * 4)
    ])
    def test_strstrb(self, str2, expected):
        result = FAString(SYMBOLS).strstrb(str2)
        assert np.array_equal(result, expected)

        result = FAString(NB_PARALLEL_SYMBOLS).strstrb(str2)
        assert np.array_equal(result, expected * 2000)

    @parametrize("str2, expected", [
        ('A', [0, 0, -1, -1, -1]),
        ('AA', [0, -1, -1, -1, -1]),
        ('AAPL', [0, -1, -1, -1, -1]),
        ('', [0] * 5),
        ('AAA', [-1] * 5),
        ('B', [-1, -1, 1, -1, 1])
    ])
    def test_strstr(self, str2, expected):
        result = FAString(SYMBOLS).strstr(str2)
        assert np.array_equal(result, expected)

        result = FAString(NB_PARALLEL_SYMBOLS).strstr(str2)
        assert np.array_equal(result, expected * 2000)

    def test_strstr_cat(self):
        result = self.cat_symbol.str.strstr('A')
        expected = FA([np.iinfo(np.int32).min, 0, 0, -1, -1, -1] * 3)
        assert np.array_equal(result, expected)

    def test_strlen_cat(self):
        result = self.cat_symbol.str.strlen
        expected = FA([np.iinfo(np.int32).min, 4, 4, 2, 4, 3] * 3)
        assert np.array_equal(result, expected)

    def test_strpbrk_cat(self):
        result = self.cat_symbol.str.strpbrk('PZG')
        expected = FA([np.iinfo(np.int32).min, 2, 2, -1, 0, -1] * 3)
        assert np.array_equal(result, expected)

    regexpb_test_cases = parametrize('str2, expected', [
        ('.', [True] * 5),
        ('\.', [False] * 5),
        ('A', [True, True, False, False, False]),
        ('[A|B]', [True, True, True, False, True]),
        ('B$', [False, False, True, False, False]),
    ])

    @regexpb_test_cases
    def test_regexpb(self, str2, expected):
        fa = FA(SYMBOLS)
        assert np.array_equal(fa.str.regexpb(str2), expected)

    @regexpb_test_cases
    def test_regexpb_cat(self, str2, expected):
        cat = Cat(SYMBOLS * 2)   # introduce duplicity to test ikey properly
        assert np.array_equal(cat.str.regexpb(str2), expected * 2)
