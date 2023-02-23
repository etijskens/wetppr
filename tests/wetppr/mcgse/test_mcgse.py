#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for sub-module wetppr.mcgse."""

import pytest
import numpy as np
from math import isclose
import matplotlib
import platform
if platform.system() == 'Darwin':
    matplotlib.use('MacOSX')

import matplotlib.pyplot as plt
print(f"matplotlib.pyplot: backend = {plt.get_backend()}")

from pathlib import Path
import sys, os
p = Path(__file__).parent.parent.parent.parent
# print(p)
if not str(p) in sys.path:
    sys.path.insert(0, str(p))

import wetppr.mcgse as mcgse

# ==============================================================================
# mcgse.morse_potential tests. 
# ==============================================================================
def test_graph():
    """Not really an automated test. Draw a graph of the potential."""
    x = np.linspace(0,5,1001)[1:]
    y = mcgse.morse_potential(x)
    # plot
    fig, ax = plt.subplots()
    ax.plot(x, y)
    # plt.show()
    p = Path(__file__).parent.parent.parent.parent / 'docs' / 'public' / 'morse.png'
    print(f"savefig to {p=}")
    plt.savefig(p)


def test_morse_potential_mathematical_properties():
    n = 100
    # between 0 and 1 the curve is monotonously descending
    rn = np.random.rand(n) # in [0,1]
    x = np.copy(rn)
    y = mcgse.morse_potential(x)
    for i in range(0,n):
        for j in range(i-1):
            assert (x[j] - x[i]) / (y[j] - y[i]) < 0
    assert False
    # between 0 and 1 the second derivative is positive
    def ddy(x0,x2):
        """Finite difference approximation of second derivative"""
        x1 = (x0 + x2) / 2
        h2 = (x1 - x0) ** 2
        y0 = mcgse.morse_potential(x0)
        y1 = mcgse.morse_potential(x1)
        y2 = mcgse.morse_potential(x2)
        ddy_dx2 = (y0 - 2 * y1 + y2) / h2
        return ddy_dx2

    for i in range(0,n):
        for j in range(i-1):
            ddy_dx2 = ddy(min(x[i],x[j]), max(x[i],x[j]))
            assert ddy_dx2 > 0

    # between 1 and 1 - ln(1/2) (location of inflection point) the second derivative is positive
    x_inflection_point = 1. - np.log(0.5)
    w = x_inflection_point - 1.
    x = np.copy(rn)
    x *= w
    x += 1.
    for i in range(0,n):
        for j in range(i-1):
            ddy_dx2 = ddy(min(x[i],x[j]), max(x[i],x[j]))
            assert ddy_dx2 > 0

    # beyond 1 - ln(1/2) (location of inflection point) the second derivative is negative
    x = np.copy(rn)
    x *= 10
    x += x_inflection_point
    for i in range(0,n):
        for j in range(i-1):
            ddy_dx2 = ddy(min(x[i],x[j]), max(x[i],x[j]))
            assert ddy_dx2 < 0

    # between 1 and +infinty the curve is monotonously ascending
    x = np.copy(rn)
    x *= 10 # x in [0,10]
    x += 1  # x in [1,11]
    y = mcgse.morse_potential(x)
    for i in range(0,n):
        for j in range(i-1):
            assert (x[j] - x[i]) / (y[j] - y[i]) > 0

    # between 1 and +infinty the curve is below 1
    for i in range(0,n):
        assert y[i] <= 1.

    # the value at r=1 is 0
    x = 1
    y = mcgse.morse_potential(x)
    assert isclose(y, 0., rel_tol=1e-15)

# ==============================================================================
# mcgse.interatomic_distances tests.
# ==============================================================================
def test_interatomic_distances():
    n_atoms = 10
    x = np.array([i for i in range(n_atoms)], dtype=float)
    y = np.zeros(n_atoms, dtype=float)
    z = np.zeros(n_atoms, dtype=float)
    # the distance between i and j is i - j

    for repeat in range(3):
        rij = mcgse.interatomic_distances(x,y,z)
        ij = 0
        for i in range(1,10):
            for j in range(i):
                result = rij[ij]
                expected = i - j
                assert result == expected
                ij += 1
        # rotate x,y,z to check symmetry in interatomic distances.
        t = x
        x = y
        y = z
        z = t


def test_perturb():
    n_atoms = 10
    x = np.zeros(n_atoms, dtype=float)
    y = np.zeros(n_atoms, dtype=float)
    z = np.zeros(n_atoms, dtype=float)

    class Dist:
        def __call__(self, n=1):
            return 1

    i = mcgse.perturb(x, y, z, i=2, dist=Dist())
    for j in range(n_atoms):
        rj = np.sqrt(x[j]**2 + y[j]**2 + z[j]**2)
        expected = 1. if (j == i) else 0.
        assert isclose(rj, expected, rel_tol=1e-15)

    i = mcgse.perturb(x, y, z, i=i, dist=Dist())
    for j in range(n_atoms):
        rj = np.sqrt(x[j]**2 + y[j]**2 + z[j]**2)
        expected = 2. if (j == i) else 0.
        assert rj <= expected

    x[i] = y[i] = z[i] = 0.
    i = mcgse.perturb(x, y, z, dist=Dist())
    for j in range(n_atoms):
        rj = np.sqrt(x[j]**2 + y[j]**2 + z[j]**2)
        expected = 1. if (j == i) else 0.
        assert isclose(rj, expected, rel_tol=1e-15)


def test_energy():
    class Dist:
        def __call__(self, n=1):
            return .1
    import copy
    n_atoms = 10
    x = np.array([i for i in range(n_atoms)], dtype=float)
    y = np.zeros(n_atoms, dtype=float)
    z = np.zeros(n_atoms, dtype=float)
    # the distance between i and j is i - j
    E, Eij, rij = mcgse.energy_loop(x,y,z)  # the first time energy_loop is necessary
    i = mcgse.perturb(x, y, z, i=4, dist=Dist())
    E_loop,_,_ = mcgse.energy_loop(x, y, z) # enery_loop using the perturbed coordinates
    E_updt = copy.copy(E)
    E_updt = mcgse.energy_update(x, y, z, i, rij, Eij, E_updt) # compute interaction energy with energy_update
    print(E_updt, E_loop, E_updt-E_loop)
    assert isclose(E_updt, E_loop, rel_tol=1e-15) # rel_tol=1e-15 might be a little small



def plot_lognormal_distribution():
    # x = np.random.lognormal(size=1000, sigma=.3, mean=-5.)
    from functools import partial
    dist = mcgse.LogNormal(mean=-5, sigma=.4)
    x = dist(1000)
    num_bins = 100
    n, bins, patches = plt.hist(x, num_bins, facecolor='blue', alpha=0.5)
    plt.show()


# def try_partial(size):
#     dist = partial(np.random.lognormal, mean=-5, sigma=.3)
#     return dist(size)

# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (normally all tests are run with pytest)
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_morse_potential_mathematical_properties

    print("__main__ running", the_test_you_want_to_debug)
    the_test_you_want_to_debug()
    print("-*# finished #*-")
# ==============================================================================
