# Exercise 1 - Getting started with `wip` - Dot product implementations

## Preconditions

- You have **Python 3.9** or higher on your system.
- You have a **GitHub account**. If you don't, create one
  [here](https://docs.github.com/en/get-started/signing-up-for-github/signing-up-for-a-new-github-account).
- You have a (classic) **GitHub personal access token**. If not, you can create a (classic) personal access
  token following [these instructions](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic)
  Make sure you check at least the scopes `repo` and `read:org`.
- `wiptools` must be installed ([Installation instructions here](https://etijskens.github.io/wiptools/installation)).

## Assignment

This assignment must be carried out on your ***local*** system.

1. Construct a Python module with function for the dot product $\sum_{i=1}^{n}{a_i}{b_i}$ of two
   arrays $a$ and $b$. Start out with a Python implementation. Use a  
   [Python list](https://docs.python.org/3/library/stdtypes.html?highlight=list#list)
   for representing arrays.

2. Time the Python implementation for a range of array lengths.

3. Try improving the timings by using the [numba](https://numba.readthedocs.io/en/stable/) `@jit`
   decorator. Tip: use Numpy's
   [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.array.html)
   for storing arrays instead of a
   [Python list](https://docs.python.org/3/library/stdtypes.html?highlight=list#list).

4. Try improving the code by providing your own C++ and/or Modern Fortran implementation. Again use
   Numpy [arrays](https://numpy.org/doc/stable/reference/generated/numpy.array.html) instead of
   Python [list](https://docs.python.org/3/library/stdtypes.html?highlight=list#list).

5. Compare your implementations with
   [numpy's own dot product](https://numpy.org/doc/stable/reference/generated/numpy.dot.html) `numpy.dot`.

6. Report all timings and explain your observations in the `README.md` file.

7. Store you project files on GitHub.

## Solution

Although the dot product is an extremely simple concept, this exercise is more involved than one
would expect. The [solution](exercise-1-solution.md) also demonstrates our software development
strategy developed in [chapter 5][a-strategy-for-the-development-research-software].
