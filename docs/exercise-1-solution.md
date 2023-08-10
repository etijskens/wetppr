# Exercise 1 - Getting started with `wip`

## 1. A simple Python module with a method to compute the dot product of two arrays 

### Setting up a `wip` project

We must first choose a name for our project, _e.g._ `Dot`. We create a `Dot` project in our workspace 
directory. We are assuming that our environment has Python and `wip` installed.

```shell
> cd workspace
> wip init Dot

Project info needed:
Enter a short description for the project: [<project_short_description>]: dot product implementations
Enter the minimal Python version [3.9]:

[[Expanding cookiecutter template `/Users/etijskens/software/dev/workspace/wiptools/wiptools/cookiecutters/project` ...
]] (done Expanding cookiecutter template `/Users/etijskens/software/dev/workspace/wiptools/wiptools/cookiecutters/project`)

[[Creating a local git repo ...

[[Running `git init --initial-branch=main` in project folder Dot ...
Initialized empty Git repository in /Users/etijskens/software/dev/workspace/Dot/.git/
]] (done Running `git init --initial-branch=main`)

[[Running `git add *` in project folder Dot ...
]] (done Running `git add *`)

[[Running `git add .gitignore` in project folder Dot ...
]] (done Running `git add .gitignore`)

[[Running `git commit -m "Initial commit from wip init Dot"` in project folder Dot ...
[main (root-commit) fbcb8a9] Initial commit from wip init Dot
 7 files changed, 226 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 CHANGELOG.md
 create mode 100644 README.md
 create mode 100644 dot/__init__.py
 create mode 100644 pyproject.toml
 create mode 100644 tests/dot/test_dot.py
 create mode 100644 wip-cookiecutter.json
]] (done Running `git commit -m "Initial commit from wip init Dot"`)
]] (done Creating a local git repo)
```

After providing a short project description and accepting the default minimal Python version, `wip`
sets up the project directory. We `cd` into the `Dot` project directory, because that's where we will 
be working, and tools as `wip` and `git` look for file in the project directory.

```shell
> cd Dot
```

`Wip` has created quite a bit of files for us:

```shell
> tree
.
├── .bumpversion.cfg # coonfiguration file for bump2version (version management)
├── .git             # The local git repo ((contents not shown)
├── .gitignore       # a list of filename to be ignored by git
├── CHANGELOG.md     # list your project changes here 
├── README.md        # users should look here to get started with the dot package
├── dot              # the Python package we are creating
│   └── __init__.py
├── pyproject.toml   # project configuration file used by poetry
├── tests            # unit-tests go here
│   └── dot
│       └── test_dot.py 
└── wip-cookiecutter.json # project configuration file used by wip itself+
```

The Python package `dot` is not empty. It has a working `hello` method that serves as an example. The
`tests/dot/test_dot.py` contains some working tests for this `hello` method. In general, `wip` always 
creates files and components with working parts that show you how things are supposed to work and can
be extended easily. 

### A first dot product implementation

Use your favourite editor to edit the file `dot/__init__.py`, remove the `hello` method and add a `dot`
method that implements the mathmatical formula

$$
{a}\cdot{b} = \sum_{i=1}^{n}{a_i}{b_i}
$$

!!! Note
    [vscode](https://code.visualstudio.com) is recommended, both for local and remote editing. It 
    also offers a nice and intuitive run and debug environment.

Here is a first implementation for the dot product of two arrays:

```python
# -*- coding: utf-8 -*-
# File dot/__init__.py
"""
## Python package dot

Provides several implementations of the dot product of two arrays.
"""

__version__ = '0.0.0'

def dot(a, b):
    """Compute the dot product of a and b

    Args:
        a: array of numbers
        b: array of numbers, of same length as a
    Returns:
        the dot product of a and b 
    """
    d = 0
    for i in range(len(a)):
        d += a[i] * b[i]
    return d
```


Note that the `dot` method above is agnostic about the types of `a` and `b`. It only assumes the 
existence of an indexing operator `[]`. The implementation is also not foolproof. It assumes that the 
multiplication operator `*` is valid for all `a[i]` and `b[i]`, but it does not perform any validation
on the arguments, neither can it assure that the return value is a number indeed, as promised by the 
doc-string. However flawed this implementation is, it is a start. Testing should expose the flaws, and
we should feel urged to correct them. 

### Unit testing

Together with the package file `dot/__init__.py`, `wip` has also created a test file for it, 
`tests/dot/test_dot.py`. As a first simple test we could choose two arrays for which we can compute the 
dot product by hand easily and check that our `dot` method gives indeed the right result:

```python
# File tests/dot/test_dot.py
from dot import dot
def test_dot_aa():
    a = [1, 2, 3]
    expected = 1 + 4 + 9
    result = dot(a,a)
    assert result == expected
```

The command `pytest tests` will discover ([learn how](https://docs.pytest.org/en/7.4.x/explanation/goodpractices.html#test-discovery)) 
all tests in the `tests` directory, run them and report whether they succeeded or failed and in case of 
failure, provide some indication of what went wrong.

```shell
> pytest tests
========================================= test session starts =========================================
platform darwin -- Python 3.9.5, pytest-7.4.0, pluggy-1.2.0
rootdir: /Users/etijskens/software/dev/workspace/Dot
collected 1 item

tests/dot/test_dot.py .                                                                         [100%]

========================================== 1 passed in 0.01s ==========================================
```

The output shows that pytest discovered 1 test file, `tests/dot/test_dot.py`, with one test. Every 
successful test shows up as a `.`, a failed test as `F`. This test passed. If you want a more detailed 
output, you can pass in the `-v` option. Output from the test methods is generally suppressed by `pytest`. 
Pass in `-s` to not suppress the output. 

Obviously, our test tests only one specific case of the infinite set of possible arguments.  
Writing good tests is not easy. When dealing with mathematical concepts, like the dot product, it is 
practical to focus on mathematical properties. _E.g._ the dot product is commutative. Let's write a test 
that verifies commutativity. Rather that trying a single argument, we generate 1000 pairs of random 
arrays. We also choose a random array size in $[0,20]$ for every pair.

```python
# File tests/dot/test_dot.py
from dot import dot
import random
def test_dot_commutative():
    # Fix the seed for the random number generator of module random.
    random.seed(0)
    # repeat the test 1000 times:
    for _ in range(1000):
        # choose a random array size
        n = random.randint(0,20)
        # generate two random arrays
        a = [random.random() for i in range(n)]
        b = [random.random() for i in range(n)]
        # test commutativity:
        ab = et_dot.dot(a,b)
        ba = et_dot.dot(b,a)
        assert ab == ba
```

Let's run the tests:

```shell

> pytest tests
========================================= test session starts =========================================
platform darwin -- Python 3.9.5, pytest-7.4.0, pluggy-1.2.0
rootdir: /Users/etijskens/software/dev/workspace/Dot
collected 2 items

tests/dot/test_dot.py ..                                                                        [100%]

========================================== 2 passed in 0.06s ==========================================
```

This test passes too. Note that we fixed the seed of the random number generator. This way the test
generates the same 1000 pairs of random arrays at every run. If, _e.g._, pair 134 would fail the test, 
it will fail every time we run it. Hence, we can run it again in debug mode, and examine the cause of 
the failure. Without fixing the seed every run will generate a different sequence of array pairs, and 
we would lose the ability to reproduce a failure.

Another property of the dot product is that the dot product with an array of zeroes yelds zero, and 
with an array of ones yields the sum of the other array. Here are the test methods:

```python
def test_a_zero():
    # Fix the seed for the random number generator of module random.
    random.seed(0)
    # repeat the test 1000 times:
    for _ in range(1000):
        # choose a random array size
        n = random.randint(0,20)
        # generate two random arrays
        a = [random.random() for i in range(n)]
        zero = [0 for i in range(n)]
        # test commutativity:
        a_dot_zero = et_dot.dot(a, zero)
        assert a_dot_zero == 0
        zero_dot_a = et_dot.dot(zero, a)
        assert zero_dot_a == 0

def test_a_one():
    # Fix the seed for the random number generator of module random.
    random.seed(0)
    # repeat the test 1000 times:
    for _ in range(1000):
        # choose a random array size
        n = random.randint(0,20)
        # generate two random arrays
        one = [1 for i in range(n)]
        a = [random.random() for i in range(n)]
        sum_a = sum(a)
        # test 
        a_dot_one = et_dot.dot(a, one)
        assert a_dot_one == sum_a
        one_dot_a = et_dot.dot(one, a)
        assert one_dot_a == sum_a
```

Also these succeed:

```shell
> pytest tests
========================================= test session starts =========================================
platform darwin -- Python 3.9.5, pytest-7.4.0, pluggy-1.2.0
rootdir: /Users/etijskens/software/dev/workspace/Dot
collected 4 items

tests/dot/test_dot.py ....                                                                      [100%]

========================================== 4 passed in 0.10s ==========================================
```


Right now our tests pass, and our confidence builds up. As mentioned before, our `dot` method does
not do any validation on the arguments, although the doc-string says that the arguments are expected
to be of the same length.

```python
>>> from dot import dot
>>> help(dot)
Help on function dot in module dot:

dot(a, b)
    Compute the dot product of a and b.

    Args:
        a: array of numbers
        b: array of numbers, of same length as a
    Returns:
        the dot product of a and b 
```

Here's a test for commutativity of the `dot` method with two arrays of different length:

```python
def test_different_length():
    a = [1, 2]
    b = [1, 1, 1]
    # test commutativity:
    ab = dot(a, b)
    ba = dot(b, a)
    assert ab == ba
```

When run:

```shell
> pytest tests
========================================= test session starts =========================================
platform darwin -- Python 3.9.5, pytest-7.4.0, pluggy-1.2.0
rootdir: /Users/etijskens/software/dev/workspace/Dot
collected 5 items

tests/dot/test_dot.py ....F                                                                     [100%]

============================================== FAILURES ===============================================
________________________________________ test_different_length ________________________________________

    def test_different_length():
        a = [1, 2]
        b = [1, 1, 1]
        # test commutativity:
        ab = dot(a, b)
>       ba = dot(b, a)

tests/dot/test_dot.py:74:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

a = [1, 1, 1], b = [1, 2]

    def dot(a, b):
        """Compute the dot product of a and b.

        Args:
            a: array of numbers
            b: array of numbers, of same length as a
        Returns:
            the dot product of a and b 
        """
        d = 0
        for i in range(len(a)):
>           d += a[i] * b[i]
E           IndexError: list index out of range

dot/__init__.py:21: IndexError
======================================= short test summary info =======================================
FAILED tests/dot/test_dot.py::test_different_length - IndexError: list index out of range
===================================== 1 failed, 4 passed in 0.47s =====================================
```

This test fails. Inspection of the output reveals an `IndexError` when computing `dot(b,a)`. This is
due to the `dot` method takes the loop length from the first argument, in this case 3. Since the 
second argument's length is 2 the last loop iteration (`i` being equal to 2) fails. The mathematically
inclined may argue that this is an improper use of the dot product as both arrays have different length,
and, mathematically, the dot product of `a` and `b` is not defined in that case. This could be fixed 
by verifying that both arguments have the same length and raise an exception if that is the case. 
_E.g._: 

```python
def dot(a, b):
    """Compute the dot product of a and b.

    Args:
        a: array of numbers
        b: array of numbers, of same length as a
    Returns:
        the dot product of a and b 
    Raises:
        ValueError if len(a) != len(b)
    """
    n = len(a)
    if len(b) != n:
        raise ValueError("Unequal array length.")
    d = 0
    for i in range(n):
        d += a[i] * b[i]
    return d
```

Now the test will still fail, but not instead of an `IndexError` a `ValueError` is raised as soon as 
the argument arrays have different sizes. This urges us to rewrite the test to assert that a 
`ValueError` is raised:

```python
def test_different_length():
    a = [1, 2]
    b = [1, 1, 1]
    with pytest.raises(ValueError):
        ab = dot(a, b)
    with pytest.raises(ValueError):
        ba = dot(b, a)
```
Now all tests succeed. It is important that we re-run _all_ tests, not just the failing test. There is 
always a chance that the changes to our implementation might fix one issue but create another. 

```shell
> pytest tests
========================================= test session starts =========================================
platform darwin -- Python 3.9.5, pytest-7.4.0, pluggy-1.2.0
rootdir: /Users/etijskens/software/dev/workspace/Dot
collected 5 items

tests/dot/test_dot.py .....                                                                     [100%]

========================================== 5 passed in 0.09s ==========================================
```

More pragmatic readers might argue that sometimes it may be useful that in case the two arrays have 
different length, the `dot` method returns a value corresponding to the shortest length of the arrays. 
The original test can be fixed then by modifying the implementation as follows:

```python
def dot(a, b):
    """Compute the dot product of a and b. If one of the arrays is longer than the other, the extra 
    entries are ignored. 

    Args:
        a: array of numbers
        b: array of numbers
    Returns:
        the dot product of a and b 
    """
    n = min(len(a), len(b))
    d = 0
    for i in range(n):
        d += a[i] * b[i]
    return d
```

Note that both approaches have their merits, but in the sake of clarity, it is important that the 
doc-string correctly explains what the method does. 

As shown above, useful tests can be based on mathematical properties. However, tests occasionally fail
because our expectations are typically based on the behavior of real numbers. Generally, computers use
single precision (SP) or double precision (DP) numbers, which have a finite precision. SP stores 
approximately 8 digits and DP approximately 16. The finite precision destroys some of the mathematical 
properties of real numbers we are so used to. _E.g._ what is the outcome of these dot products?

$$ \left[ \begin{array}{ccc} 1 & 1 & 1 \end{array} \right] \cdot \left[ \begin{array}{ccc} 1e16 & 1 & -1e16 \end{array} 
\right] $$

$$ \left[ \begin{array}{ccc} 1 & 1 & 1 & 1 \end{array} \right] \cdot \left[ \begin{array}{ccc} 0.1 & 0.1 & 0.1 & 1 & 
-0.3 \end{array} \right] $$

Your expectations are, rightfully, $1e16 + 1 - 1e16 = 1$ and $0.1 + 0.1 + 0.1 - 0.3 = 0$, respectively. 
However, surprisingly, Python does not agree:

```pycon
>>> from dot import dot
>>> dot([1, 1, 1], [1e16, 1, -1e16])
0
>>> dot([1, 1, 1, 1], [0.1, 0.1, 0.1, -0.3])
5.551115123125783e-17
```

The default Python type for floating point numbers is `float` and is DP. This has nothing to do with
our dot product implementation:

```pycon
>>> 1e16 + 1 - 1e16
0 
>>> 0.1 + 0.1 + 0.1 - 0.3
5.551115123125783e-17
```

Things become a little clearer when dropping the subtraction:

```pycon
>>> 1e16 + 1
1e+16
>>> 0.1 + 0.1 + 0.1
0.30000000000000004
```

The outcome of `1e16 + 1` is not `1e16 + 1` but `1e16`. Because the `1` we are adding would be the 17th 
digit, which is beyond the precision of a Python `float`, adding it has no effect and we are effectively 
computing `1e16 - 1e16`. Similarly, `0.1` and `0.3` cannot be represented exactly as a `float` and the 
errors do not cancel out. This behavior can make a test fail surprisingly, so it is important to be aware.   

Note that, contrary to the real numbres thy are supposed to represent, the addition of floating point 
numbers is NOT commutative:

```pycon
>>> 1e16 + 1 - 1e16
0 
>>> 1e16 - 1e16 + 1
1
>>> 0.1 + 0.1 + 0.1 - 0.3
5.551115123125783e-17
>>> 0.1 + 0.1 - 0.3 + 0.1
2.7755575615628914e-17
```

## 2. Timing your code

Parallel programming is about getting the maximum performance out of the machine you are computing
on. Whether that is your laptop, or a Tier-0 supercomputer does not matter. Timing your code is 
essential to evaluate its computational efficiency, and to understand the architectural features
that influence performance. 

Timing means measuring how much time it takes to execute a part of the code. The Python standard 
library `time` has the `perf_counter()` method for this. Here is a typical example.

```python
from time import perf_counter
t0 = perf_counter() 
# code to be timed
t = perf_counter() - t0
print(f'This took {t} seconds')
```

Here's a test function that performs the timing. The dot product computation is repeated a number of 
times in order to provide meaningfull results for small array sizes:

```python
from time import perf_counter

def test_time():
    n_repetitions = 10
    print(f'\ntest_time()')
    print(f'{n_repetitions=}')
    for n in [1_000, 10_000, 100_000, 1_000_000]:
        a = [random.random() for i in range(n)]
        b = [random.random() for i in range(n)]

        t0 = perf_counter()
        for _ in range(n_repetitions):
            a_dot_b = dot(a, b)
        seconds = (perf_counter() - t0) / n_repetitions
        print(f'{n=} dot(a, b) took {seconds}s')
```

Here is the output:

```shell
> pytest tests -s
========================================= test session starts =========================================
platform darwin -- Python 3.9.5, pytest-7.4.0, pluggy-1.2.0
rootdir: /Users/etijskens/software/dev/workspace/Dot
collected 6 items

tests/dot/test_dot.py .....
test_time()
n_repetitions=10
n=1000 dot(a, b) took 0.00026637590000000433s
n=10000 dot(a, b) took 0.0022314830000000007s
n=100000 dot(a, b) took 0.017176923499999996s
n=1000000 dot(a, b) took 0.1444069864s
.

========================================= 6 passed in 10.63s ==========================================
```

## 3.Using numba for speeding up your code

Python is notoriously slow at executing loops. Moreover, the Python `list` is an extremely flexible 
data structure, mimicking an array (it has an indexing operator that takes an integer). Actually, it
is and array of pointers, each of which may point to an arbitrary type. As a consequence, iterating over 
a Python `list` is extra slow because it does not use the cache optimally. A true array is a contiguous 
piece of memory where each entry has the same data type.  Numpy 
[arrays](https://numpy.org/doc/stable/reference/generated/numpy.array.html) are extremly useful for 
scientific computing. The Numba [jit] decorator takes a Python method, translates the code into C and 
compiles it. Together with a contiguous data structure this can achieve significant speedups.

### A Numba accelerated version of the `dot` method

The standard way to create a Numba accelerated version of a method is to precede its definition with
the `@jit` decorator:

```python
from numba import jit
@jit
def dot(a, b):
    ...

```

The first time the `dot` method is called, it is compiled and then applied. All subsequent calls directly
apply the compiled version. The decorator approach hides the original Python version. This is impractical 
if we want to compare the timings of both versions. We can keep both versions like this:

```python
# File dot/__init__.py
from numba import jit
def dot(a, b):
    ...

nb_dot = jit(dot)
```

If we want the Python version, we call `dot`, the `numba.jit` accelerated version is called as `nb_dot`.

Let's add a timing function to our tests (using Numpy arrays instead of Python lists):

```python
import numpy as np
def test_time_numba():
    print(f'\ntest_time_numba()')
    n_repetitions = 10
    print(f'{n_repetitions=}')
    for n in [1_000, 10_000, 100_000, 1_000_000]:
        # a = [random.random() for i in range(n)] 
        # b = [random.random() for i in range(n)]
        # python lists are replaced with numpy arrays
        a = np.random.random(n)
        b = np.random.random(n)
        t0 = perf_counter()
        for _ in range(n_repetitions):
            a_dot_b = nb_dot(a, b)
        seconds = (perf_counter() - t0) / n_repetitions
        print(f'{n=} dot(a, b) took {seconds}s')
```

Here are the timings:

```shell
> pytest tests -s
========================================= test session starts =========================================
platform darwin -- Python 3.9.5, pytest-7.4.0, pluggy-1.2.0
rootdir: /Users/etijskens/software/dev/workspace/Dot
collected 8 items

tests/dot/test_dot.py .....
test_time()
n_repetitions=10
n=1000 dot(a, b) took 9.876120000000821e-05s
n=10000 dot(a, b) took 0.0012254463999999965s
n=100000 dot(a, b) took 0.011126110799999988s
n=1000000 dot(a, b) took 0.1173576513s
.
test_time_numba()
n_repetitions=10
n=1000 dot(a, b) took 0.055231137799999885s
n=10000 dot(a, b) took 1.419590000004689e-05s
n=100000 dot(a, b) took 0.00015608759999992118s
n=1000000 dot(a, b) took 0.0019177367999999363s
.

==================================== 8 passed, 1 warning in 10.99s ====================================
```

The speedup for the largest arrays is 0.1174/0.001918 = 61.20. 

##

At this point is  