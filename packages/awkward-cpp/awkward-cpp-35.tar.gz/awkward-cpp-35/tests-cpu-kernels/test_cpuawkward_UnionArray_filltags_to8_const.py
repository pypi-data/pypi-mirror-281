# AUTO GENERATED ON 2024-06-26 AT 17:00:14
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import ctypes
import numpy as np
import pytest

from awkward_cpp.cpu_kernels import lib

def test_cpuawkward_UnionArray_filltags_to8_const_1():
    totags = [123, 123, 123, 123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    totagsoffset = 3
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray_filltags_to8_const')
    ret_pass = funcC(totags, totagsoffset, length, base)
    pytest_totags = [123, 123, 123, 3, 3, 3]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

