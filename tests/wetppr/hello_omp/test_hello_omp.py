#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for C++ module wetppr.hello_omp.
"""
import os
import sys
sys.path.insert(0,'.')
sys.path.insert(0,'../../..')

import numpy as np

from wetppr.hello_omp import hello_omp, hello_omp_from, get_cpu, get_proc_ids, info


def test_hello_omp():
    hello_omp()

def test_hello_omp_from():
    hello_omp_from(0)
    
def test_get_cpu():
    aff = os.sched_getaffinity(0)
    cpu = get_cpu()
    print(f"'{aff=}' ?= '{cpu=}'")
    assert aff == cpu 

def test_get_proc_ids():
    # ids = -np.ones(64, dtype=np.intc)
    # print(f"{ids=}")
    # get_proc_ids(ids)
    # print(f"{ids=}")
    info(-1)

#===============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (normally all tests are run with pytest)
#===============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_get_proc_ids

    print(f"__main__ running {the_test_you_want_to_debug} ...")
    the_test_you_want_to_debug()
    print('-*# finished #*-')
#===============================================================================
