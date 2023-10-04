# Exercise 1 - Getting started with `wip`

## 1. A simple Python module with a method to compute the dot product of two arrays

### Setting up a `wip` project

We must first choose a name for our project, _e.g._ `Dot`. We create a `Dot` project in our
workspace directory. We are assuming that our environment has Python and `wip` installed.

```shell
> cd workspace
> wip init Dot

Project info needed:
Enter a short description for the project: [<project_short_description>]: dot product
implementations Enter the minimal Python version [3.9]:

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
sets up the project directory. We `cd` into the `Dot` project directory, because that's where the
work will be done, and tools as `wip` and `git` look for file in the project directory.

```shell
> cd Dot
```

!!! tip
    By default `wip` creates a _public_ remote GitHub repo. If you want it to be private add the
    flag `--remote=private` to the `wip init` command. If you do not want a remote repo, add
    `--remote=none` (not recommended).


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

The Python package `dot` is not empty. It has a working `hello` method that serves as an example.
The `tests/dot/test_dot.py` contains some working tests for this `hello` method. In general, `wip`
always creates files and components with working parts that show you how things are supposed to work
and can be extended easily.

### A first dot product implementation

Use your favourite editor to edit the file `dot/__init__.py`, remove the `hello` method and add a
`dot` method that implements the mathmatical formula

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
existence of an indexing operator `[]`. The implementation is also not foolproof. It assumes that
the multiplication operator `*` is valid for all `a[i]` and `b[i]`, but it does not perform any
validation on the arguments, neither can it assure that the return value is a number indeed, as
promised by the doc-string. However flawed this implementation is, it is a start. Testing should
expose the flaws, and we should feel urged to correct them.

### Unit testing

Together with the package file `dot/__init__.py`, `wip` has also created a test file for it,
`tests/dot/test_dot.py`. As a first simple test we could choose two arrays for which we can compute
the dot product by hand easily and check that our `dot` method gives indeed the right result:

```python
# File tests/dot/test_dot.py
from dot import dot
def test_dot_aa():
    a = [1, 2, 3]
    expected = 1 + 4 + 9
    result = dot(a,a)
    assert result == expected
```

The command `pytest tests` will discover
([learn how](https://docs.pytest.org/en/7.4.x/explanation/goodpractices.html#test-discovery))
all tests in the `tests` directory, run them and report whether they succeeded or failed and in case
of failure, provide some indication of what went wrong.

```shell
> pytest tests
======================================== test session starts =======================================
platform darwin -- Python 3.9.5, pytest-7.4.0, pluggy-1.2.0
rootdir: /Users/etijskens/software/dev/workspace/Dot
collected 1 item

tests/dot/test_dot.py .                                                                       [100%]

========================================= 1 passed in 0.01s ========================================
```

The output shows that pytest discovered 1 test file, `tests/dot/test_dot.py`, with one test. Every
successful test shows up as a `.`, a failed test as `F`. This test passed. If you want a more
detailed output, you can pass in the `-v` option. Output from the test methods is generally
suppressed by `pytest`. Pass in `-s` to not suppress the output.

Obviously, our test tests only one specific case of the infinite set of possible arguments.  
Writing good tests is not easy. When dealing with mathematical concepts, like the dot product, it is
practical to focus on mathematical properties. _E.g._ the dot product is commutative. Let's write a
test that verifies commutativity. Rather that trying a single argument, we generate 1000 pairs of
random arrays. We also choose a random array size in $[0,20]$ for every pair.

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
======================================= test session starts ========================================
platform darwin -- Python 3.9.5, pytest-7.4.0, pluggy-1.2.0
rootdir: /Users/etijskens/software/dev/workspace/Dot
collected 2 items

tests/dot/test_dot.py ..                                                                     [100%]

========================================= 2 passed in 0.06s ========================================
```

This test passes too. Note that we fixed the seed of the random number generator. This way the test
generates the same 1000 pairs of random arrays at every run. If, _e.g._, pair 134 would fail the
test, it will fail every time we run it. Hence, we can run it again in debug mode, and examine the
cause of the failure. Without fixing the seed every run will generate a different sequence of array
pairs, and we would lose the ability to reproduce a failure.

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
======================================= test session starts ========================================
platform darwin -- Python 3.9.5, pytest-7.4.0, pluggy-1.2.0
rootdir: /Users/etijskens/software/dev/workspace/Dot
collected 4 items

tests/dot/test_dot.py ....                                                                    [100%]

======================================== 4 passed in 0.10s =========================================
```

As our tests pass,  our confidence builds up. As mentioned before, our `dot` method does not do any
validation on the arguments, although the doc-string says that the arguments are expected to be of
the same length.

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
======================================= test session starts ========================================
platform darwin -- Python 3.9.5, pytest-7.4.0, pluggy-1.2.0
rootdir: /Users/etijskens/software/dev/workspace/Dot
collected 5 items

tests/dot/test_dot.py ....F                                                                   [100%]

============================================ FAILURES ==============================================
______________________________________ test_different_length _______________________________________

    def test_different_length():
        a = [1, 2]
        b = [1, 1, 1]
        # test commutativity:
        ab = dot(a, b)
>       ba = dot(b, a)

tests/dot/test_dot.py:74:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

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
===================================== short test summary info ======================================
FAILED tests/dot/test_dot.py::test_different_length - IndexError: list index out of range
=================================== 1 failed, 4 passed in 0.47s ====================================
```

This test fails. Inspection of the output reveals an `IndexError` when computing `dot(b,a)`. This
is due to the `dot` method takes the loop length from the first argument, in this case 3. Since the
second argument's length is 2 the last loop iteration (`i` being equal to 2) fails. The
mathematically inclined may argue that this is an improper use of the dot product as both arrays
have different length, and, mathematically, the dot product of `a` and `b` is not defined in that
case. This could be fixed by verifying that both arguments have the same length and raise an
exception if that is the case. _E.g._:

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

Now the test will still fail, but instead of an `IndexError` a `ValueError` is raised as soon
as the argument arrays have different sizes. This urges us to rewrite the test to assert that a
`ValueError` is raised, because that is the expected behavior:

```python
def test_different_length():
    a = [1, 2]
    b = [1, 1, 1]
    with pytest.raises(ValueError):
        ab = dot(a, b)
    with pytest.raises(ValueError):
        ba = dot(b, a)
```

All tests succeed. It is important that we re-run _all_ tests, not just the failing test. There
is always a chance that changes to our implementation might fix one issue but create another.

```shell
> pytest tests
======================================= test session starts ========================================
platform darwin -- Python 3.9.5, pytest-7.4.0, pluggy-1.2.0
rootdir: /Users/etijskens/software/dev/workspace/Dot
collected 5 items

tests/dot/test_dot.py .....                                                                  [100%]

======================================== 5 passed in 0.09s =========================================
```

More pragmatic readers might argue that sometimes it may be useful that in case the two arrays have
different length, the `dot` method returns a value corresponding to the shortest length of the
arrays. The original test can be fixed then by modifying the implementation as follows:

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

As shown above, useful tests can be based on mathematical properties. However, tests occasionally
fail because our expectations are typically based on the behavior of real numbers. Generally,
computers use single precision (SP) or double precision (DP) numbers, which have a finite precision.
SP stores approximately 8 digits and DP approximately 16. The finite precision destroys some of the
mathematical properties of real numbers we are so used to. _E.g._ what is the outcome of these dot
products?

$$ \left[ \begin{array}{ccc} 1 & 1 & 1 \end{array} \right] \cdot \left[ \begin{array}{ccc} 1e16 & 1
& -1e16 \end{array} \right] $$

$$ \left[ \begin{array}{ccc} 1 & 1 & 1 & 1 \end{array} \right] \cdot \left[ \begin{array}{ccc}
0.1 & 0.1 & 0.1 & 1 & -0.3 \end{array} \right] $$

Your expectations are, rightfully, $1e16 + 1 - 1e16 = 1$ and $0.1 + 0.1 + 0.1 - 0.3 = 0$,
respectively. However, surprisingly, Python does not agree:

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

The outcome of `1e16 + 1` is not `1e16 + 1` but `1e16`. Because the `1` we are adding would be the
17th digit, which is beyond the precision of a Python `float`, adding it has no effect and we are
effectively computing `1e16 - 1e16`. Similarly, `0.1` and `0.3` cannot be represented exactly as a
`float` and the errors do not cancel out. This behavior can make a test fail surprisingly, so it is
important to be aware.   

Note that, contrary to the real numbres thy are supposed to represent, the addition of floating
point numbers is NOT commutative:

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
======================================== test session starts =======================================
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

======================================== 6 passed in 10.63s ========================================
```

## 3.Using numba for speeding up your code

Python is notoriously slow at executing loops. Moreover, the Python `list` is an extremely flexible
data structure, mimicking an array (it has an indexing operator that takes an integer). Actually, it
is and array of pointers, each of which may point to an arbitrary type. As a consequence, iterating
over a Python `list` is extra slow because it does not use the cache optimally. A true array is a
contiguous piece of memory where each entry has the same data type.  Numpy
[arrays](https://numpy.org/doc/stable/reference/generated/numpy.array.html) are extremly useful for
scientific computing. The Numba [jit] decorator takes a Python method, translates the code into C
andcompiles it. Together with a contiguous data structure this can achieve significant speedups.

### A Numba accelerated version of the `dot` method

The standard way to create a Numba accelerated version of a method is to precede its definition with
the `@jit` decorator:

```python
from numba import jit
@jit
def dot(a, b):
    ...

```

The first time the `dot` method is called, it is compiled and then applied. All subsequent calls
directly apply the compiled version. The decorator approach hides the original Python version. This
is impractical if we want to compare the timings of both versions. We can keep both versions like
this:

```python
# File dot/__init__.py
from numba import jit
def dot(a, b):
    ...

jit_dot = jit(dot)
```

If we want the Python version, we call `dot.dot`, the `numba.jit` accelerated version is called as
`dot.jit_dot`.

Although we did not change the Python implementation, it is wise to subject `dot.jit_dot` to the same
tests as `dot.dot`.

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
            a_dot_b = jit_dot(a, b)
        seconds = (perf_counter() - t0) / n_repetitions
        print(f'{n=} dot(a, b) took {seconds}s')
```

Here are the timings:

```shell
> pytest tests -s
======================================== test session starts =======================================
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

=================================== 8 passed, 1 warning in 10.99s ==================================
```

The speedup for the largest arrays is 0.1174/0.001918 = 61.20.

## 4. Adding your own C++/Modern Fortran implementations

Numba proves that low-level language implementations can be significantly faster than Pythons
itself. It is not too hard to provide your own low-level implementations in C++ or Morern Fortran.
`Wip` facilitates it greatly.

### C++ implementation

First, add a C++ binary extension module to the project:

```shell
> wip add cpp_impl --cpp

[[Expanding cookiecutter template `/Users/etijskens/software/dev/workspace/wiptools/wiptools/cookiecutters/module-cpp` ...
]] (done Expanding cookiecutter template `/Users/etijskens/software/dev/workspace/wiptools/wiptools/cookiecutters/module-cpp`)

[[Expanding cookiecutter template `cookiecutters/module-cpp-tests` ...
]] (done Expanding cookiecutter template `cookiecutters/module-cpp-tests`)
```

Inspection of the project directory shows a `cpp_impl` subdirectory in the package directory `dot`
as well as in the `tests/dot` directory:

```shell
> tree
.
├── CHANGELOG.md
├── README.md
├── dot
│   ├── __init__.py
│   └── cpp_impl
│       ├── CMakeLists.txt
│       ├── cpp_impl.cpp
│       └── cpp_impl.md
├── pyproject.toml
├── tests
│   └── dot
│       ├── cpp_impl
│       │   └── test_cpp_impl.py
│       └── test_dot.py
└── wip-cookiecutter.json
```

As usual the files added by `wip` contain working example code.  Edit the file
`dot/cpp_impl/cpp_impl.cpp` as below:

```cpp
/*
 *  C++ source file for module dot.cpp_impl
 *  File dot/cpp_impl/cpp_impl.cpp
 */
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h> // add support for multi-dimensional arrays
#include <string>
namespace nb = nanobind;

double
dot
  ( nb::ndarray<double> a // in
  , nb::ndarray<double> b // in
  )
{// detect argument errors.
    if( a.ndim() != 1 )
        throw std::domain_error(std::string("Argument 1 is not a 1D-array."));
    if( b.ndim() != 1 )
        throw std::domain_error(std::string("Argument 2 is not a 1D-array."));
    size_t n = a.shape(0);
    if ( n != b.shape(0) )
        throw std::domain_error(std::string("The arguments do not have the same length."));
 // we do not intend to modify a, nor b, hence declare const
    double const * a_ = a.data();
    double const * b_ = b.data();
 // do the actual work
    double d = 0;
    for(size_t i = 0; i < n; ++i) {
        d += a_[i] * b_[i];
    }
    return d;
}

NB_MODULE(cpp_impl, m) {
    m.doc() = "A binary python extension";
    m.def("dot", &dot, "Dot product of two float 1D arrays.");
}
```

Build the binary extension module:

```shell
> wip build
C++

[[Building C++ binary extension `dot/cpp_impl` ...

[[Running `cmake -S . -B _cmake_build` in folder `dot/cpp_impl ...
-- Configuring done
-- Generating done
-- Build files have been written to: /Users/etijskens/software/dev/workspace/Dot/dot/cpp_impl/_cmake_build
]] (done Running `cmake -S . -B _cmake_build`)

[[Running `cmake --build _cmake_build` in folder `dot/cpp_impl ...
Consolidate compiler generated dependencies of target nanobind-static
[ 84%] Built target nanobind-static
Consolidate compiler generated dependencies of target cpp_impl
[ 92%] Building CXX object CMakeFiles/cpp_impl.dir/cpp_impl.cpp.o
[100%] Linking CXX shared module cpp_impl.cpython-39-darwin.so
[100%] Built target cpp_impl
]] (done Running `cmake --build _cmake_build`)

[[Running `cmake --install _cmake_build` in folder `dot/cpp_impl ...
-- Install configuration: "Release"
-- Installing: /Users/etijskens/software/dev/workspace/Dot/dot/cpp_impl/../cpp_impl.cpython-39-darwin.so
]] (done Running `cmake --install _cmake_build`)
]] (done Building C++ binary extension `dot/cpp_impl`)
```

The dot package directory now contains a dynamic library file `cpp_impl.cpython-39-darwin.so` (the
extension depends on your OS and Python version)

Add these line to the  `dot/__init__.py` file to expose the new implementation:

```python
# Expose the C++ implementation as cpp_dot
from dot.cpp_impl import dot as cpp_dot
```

Here's a test function. Ideally, all tests  devised for the initial Python implementation `dot.dot`
would be repeated for `doc.cpp_dot`.

```python
# File tests/dot/cpp_impl/test_cpp_impl.py
import numpy as np
import dot

def test_cpp_dot_one():
    a = np.array([0,1,2,3,4],dtype=float)
    b = np.ones(a.shape,dtype=float)
    expected = np.sum(a)
    d = dot.cpp_dot(a, b)
    assert d == expected
```

The test passes:

```shell
> pytest tests/dot/cpp_impl/test_cpp_impl.py
======================================== test session starts =======================================
platform darwin -- Python 3.9.5, pytest-7.4.0, pluggy-1.2.0
rootdir: /Users/etijskens/software/dev/workspace/Dot
collected 1 item

tests/dot/cpp_impl/test_cpp_impl.py .                                                         [100%]

=================================== 1 passed, 1 warning in 0.81s ===================================
```

### Modern Fortran implementation

First, add a Modern Fortran binary extension module to the project:

```shell
> wip add f90_impl --f90

[[Expanding cookiecutter template `/Users/etijskens/software/dev/workspace/wiptools/wiptools/cookiecutters/module-f90` ...
]] (done Expanding cookiecutter template `/Users/etijskens/software/dev/workspace/wiptools/wiptools/cookiecutters/module-f90`)

[[Expanding cookiecutter template `cookiecutters/module-f90-tests` ...
]] (done Expanding cookiecutter template `cookiecutters/module-f90-tests`)
```
Inspection of the project directory shows a `f90_impl` subdirectory in the package directory `dot`
as well as in the `tests/dot` directory:

```shell
> tree
.
├── CHANGELOG.md
├── README.md
├── dot
│   ├── __init__.py
│   ├── cpp_impl
│   │   ├── CMakeLists.txt
│   │   ├── cpp_impl.cpp
│   │   └── cpp_impl.md
│   ├── cpp_impl.cpython-39-darwin.so
│   └── f90_impl
│       ├── CMakeLists.txt
│       ├── f90_impl.f90
│       └── f90_impl.md
├── pyproject.toml
├── tests
│   └── dot
│       ├── cpp_impl
│       │   └── test_cpp_impl.py
│       ├── f90_impl
│       │   └── test_f90_impl.py
│       └── test_dot.py
└── wip-cookiecutter.json
```

Edit the file `dot/f90_impl/f900_impl.f90` as below:

```fortran
real*8 function dot(a,b,n)
  ! Compute the dot product of two 1d arrays.
  !
    implicit none
  !-------------------------------------------------------------------------------------------------
    integer*4              , intent(in)    :: n
    real*8   , dimension(n), intent(in)    :: a,b
  ! real*8                 , intent(out)   :: dot
    ! intent is inout because we do not want to return an array to avoid needless copying
  !-------------------------------------------------------------------------------------------------
  ! declare local variables
    integer*4 :: i
  !-------------------------------------------------------------------------------------------------
    dot = 0.0
    do i=1,n
        dot = dot + a(i) * b(i)
    end do
end function dot
```

Add this line to the file `dot/__init__.py` to expose the fortran implementation:

```python
# File dot/__init__.py
from f90_impl import dot as f90_dot
```

Add a test method:

```python
# File tests/dot/cpp_impl/test_cpp_impl.py
import numpy as np
import dot

def test_f90_dot_one():
    a = np.array([0,1,2,3,4],dtype=float)
    b = np.ones(a.shape,dtype=float)
    expected = np.sum(a)
    d = dot.f90_dot(a, b)
    assert d == expected
```

and run it:

```shell
> pytest tests/dot/f90_impl/test_f90_impl.py
======================================== test session starts =======================================
platform darwin -- Python 3.9.5, pytest-7.4.0, pluggy-1.2.0
rootdir: /Users/etijskens/software/dev/workspace/Dot
collected 1 item

tests/dot/f90_impl/test_f90_impl.py .                                                        [100%]

================================== 1 passed, 1 warning in 0.41s ====================================
```

## 5. Comparison to Numpy's dot product implementation

Let's add timing test methods for the C++ and Modern Fortran implementation, and for
[Numpy](httpps://numpy.org)'s  own [dot product implementation](https://numpy.
org/doc/stable/reference/generated/numpy.dot.html#numpy.dot).

```python
def test_time_cpp():
    print(f'\ntest_time_cpp()')
    n_repetitions = 10
    print(f'{n_repetitions=}')
    for n in [1_000, 10_000, 100_000, 1_000_000]:
        # a = [random.random() for i in range(n)]
        # b = [random.random() for i in range(n)]
        a = np.random.random(n)
        b = np.random.random(n)
        t0 = perf_counter()
        for _ in range(n_repetitions):
            a_dot_b = cpp_dot(a, b)
        seconds = (perf_counter() - t0) / n_repetitions
        print(f'{n=} dot(a, b) took {seconds}s')


def test_time_f90():
    print(f'\ntest_time_f90()')
    n_repetitions = 10
    print(f'{n_repetitions=}')
    for n in [1_000, 10_000, 100_000, 1_000_000]:
        # a = [random.random() for i in range(n)]
        # b = [random.random() for i in range(n)]
        a = np.random.random(n)
        b = np.random.random(n)
        t0 = perf_counter()
        for _ in range(n_repetitions):
            a_dot_b = f90_dot(a, b)
        seconds = (perf_counter() - t0) / n_repetitions
        print(f'{n=} dot(a, b) took {seconds}s')


def test_time_numpy():
    print(f'\ntest_time_numpy()')
    n_repetitions = 10
    print(f'{n_repetitions=}')
    for n in [1_000, 10_000, 100_000, 1_000_000]:
        # a = [random.random() for i in range(n)]
        # b = [random.random() for i in range(n)]
        a = np.random.random(n)
        b = np.random.random(n)
        t0 = perf_counter()
        for _ in range(n_repetitions):
            a_dot_b = np.dot(a, b)
        seconds = (perf_counter() - t0) / n_repetitions
        print(f'{n=} dot(a, b) took {seconds}s')

```

and run it:

```shell
> pytest tests -s

...
test_time_numba()
n_repetitions=10
n=1000 dot(a, b) took 0.13340862129999992s
n=10000 dot(a, b) took 1.2983299999902442e-05s
n=100000 dot(a, b) took 0.0001236856999998537s
n=1000000 dot(a, b) took 0.0016462048000001062s
.
test_time_cpp()
n_repetitions=10
n=1000 dot(a, b) took 4.069380000011335e-05s
n=10000 dot(a, b) took 1.2986199999787118e-05s
n=100000 dot(a, b) took 0.00012309770000022978s
n=1000000 dot(a, b) took 0.0014566837000000276s
.
test_time_f90()
n_repetitions=10
n=1000 dot(a, b) took 1.8575000002130082e-06s
n=10000 dot(a, b) took 1.2266699999941012e-05s
n=100000 dot(a, b) took 0.00011799439999968798s
n=1000000 dot(a, b) took 0.001525724200000056s
.
test_time_numpy()
n_repetitions=10
n=1000 dot(a, b) took 0.00020460570000011558s
n=10000 dot(a, b) took 5.809499999998025e-06s
n=100000 dot(a, b) took 4.74010000001357e-05s
n=1000000 dot(a, b) took 0.0006969873999999266s
...
```

Note that the C++ and Modern Fortran implementations are only marginally faster than the `numba.jit`
accelerated version, but that the numpy implementation is still 2.36 times faster. This is probably
because when compiling the former no measures were taken to ensure vectorisation. When vectorisation
is enabled, these implementations would perform similar to the numpy implementation.

### The moral of the story

1. You won't beat implementations of HPC libraries like Numpy. Specialists have gone great lengths
to ensure they squeeze out the last bit of performance out of your cpu (avoiding slow Python loops,
using the cache efficiently, using SIMD vectorisation and shared memory parallellization). Numpy
arrays perform better than Python lists because they are contiguous blocks of data items of the same
numeric type. In a Python list each entry is actually a pointer that may point to whatever object
type. When the entry is accessed, Python must first find out the data type of the object and
interpret it, before it can act on the object.
2. Python itself is bad at number crunching, especially if raw Python loops are involved.
3. You can transform Python code into low-level code using Numba and obtain significant speedups,
without much effort. Sometimes the wins are close to optimal, sometimes not. Much depends on the
data structures used in the Python implementation.
4. You can also provide your own number-crunching routines in C++ or Modern Fortran. This gives you
much more control over performance than Numba and allows you to squeeze the last bit of performance
out of your cpu, but this requires expertise in C++ and/or Modern Fortran and performance
programming principles. In principle both C++ and Modern Fortran are capable of achieving the same
performance.
5. `Wip` greatly facilitates the creation of binary extension modules for use with Python.

### How to make sure all implementations pass the same tests

This is a useful but somewhat advanced topic, illustrating using methods as objects and the concept
of generator functions. If you are a Python novice, you might want to skip this section and
[move on to section 6][6-report].

So far, all we provided separate tests and timings for all our implementations. As there is 5 of
them, this implies a lot of code duplication, which we would like to avoid. Also we might forget to
fully test all implementations, and miss bugs as a consequence. How can we subject all
implementations to the same tests, and the same timing tests?

In the example above, we have 5 different implementations which can be applied to three different
types of arrays. Let's put them in a `list`, `IMPLEMENTATIONS` (we use capitalized naming to
indicate it is a global variable).

```python
import numpy as np
from dot import *
IMPLS = [
    dot     # the initial Python implementation
  , jit_dot # numba.jit(dot)
  , cpp_dot # the C++ implementation
  , f90_dot # the Modern Fortran implementation
  , np.dot  # the Numpy implementation
]
ARRAY_TYPES = [ list, np.array ]
```

We can iterate over the list and apply the implementations to some arguments:

```python
a = ...
b = ...
for dot_impl in IMPLEMENTATIONS:
    print(f'{dot_impl(a, b)}=')
```

If all goes well, this will print 5 times the dot product of `a` and `b`.

Because the implementations are basically function pointers, their value is not very informative.
We create a `dict` that maps the values to more descriptive strings and print them:

```python
IMPLEMENTATION_DESCRIPTIONS = {
    dot    : 'python dot version',
    jit_dot: 'numba.jit()dot version',
    cpp_dot: 'C++ dot version',
    f90_dot: 'f90 dot version',
    npy_dot: 'numpy.dot version',
}
print("\nList of implementations:")
print("\nImplementation descriptions:")
for dot_impl, desc in IMPLEMENTATION_DESCRIPTIONS.items():
    print(f'{str(dot_impl) : <44} {desc:>20}')
print()
```

The print statements yield the following output:

```shell
Implementation descriptions:
<function dot at 0x1085efd30>                     python dot implementation
CPUDispatcher(<function dot at 0x1085efd30>) numba.jit() dot implementation
<nanobind.nb_func object at 0x10b957540>             C++ dot implementation
<fortran dot>                                        f90 dot implementation
<function dot at 0x10794e280>                      numpy.dot implementation
```

When we run the tests with `pytest`, a failing test will be reported printing the values of all
variables in the context, including the implementation that failed (the value of `dot_impl`), and
we can look up its value in the table above.

Additionally, these implementations can be applied to both Python `list`s and Numpy `ndarray`s,
except for the C++ implementation `cpp_impl`, which can only handle Numpy `array`s. This complicates
things. Either the tests must know the implementation and do something sensible when an
implementation is presented a non-supported array type, or the code generating the arrays must avoid
generating unsupported array type for each implementation. Preferentially, this should happen in a
generic way, rather than as an _ad hoc_ treatment. A generic approach means that the code has some
way of discovering which array types are valid for which implementations, without hard coding any
exceptional cases. This can be implemented using a `dict` listing the acceptable array types for
each implementation:

```python
IMPLEMENTATION_ARRAY_TYPES = {
    dot     : [np.ndarray, list]
  , jit_dot : [np.ndarray, list]
  , cpp_dot : [np.ndarray,]
  , f90_dot : [np.ndarray, list]
  , np.dot  : [np.ndarray, list]
}
```

This approach can be easily extended, when new implementations or array types are added.

Let's look at how the code can use these data structures. We want to automate two different things,
tests, and timings. A test needs to be executed only once, whereas for timings it is often useful
to repeat many times to obtain meaningful timings. Test methods thus have this signature:

```python
def test_it(dot_impl, a, b):
    """Test some property of the dot product for arrays `a` and `b`, admissible array types, using
    dot product implemtentation `dot_impl`."""
```

Using the framework of `tests/dot/test_dot_impls.py` tests are as simple as:

```python
def test_dot_commutative():
    """The test driver for commutativity of dot product implementations"""

    # a locally defined method testing commutativity
    def assert_dot_commutative(dot_impl, a, b):
        """The test itself"""
        ab = dot_impl(a, b)
        ba = dot_impl(b, a)
        assert ab == ba

    # run the test for all implementations and all array pairs generated by
    # _random_array_pair_generator
    _test(assert_dot_commutative
         , implementations=IMPLEMENTATIONS
         , array_pair_generator=_random_array_pair_generator(n=2)
         )
```

`_test` is a helper function defined in the same file.

## 6. Report

Report all timings in and explain your obsservations in the `README.md` file.
See [The moral of the story][the-moral-of-the-story] above.

The extension `.md` implies the Markdown file format allowing for
[simple text formatting instructions](https://www.markdownguide.org). GitHub understands MarkDown,
and displays the formatted version when you check `.md` files on https://github.com. This course
text is written entirely in MarkDown.

## 7. Storing your project files on GitHub

`Git` is a Version Control system. One of the main advantages is that it is a backup of all the
different versions of your project that you committed.

In the terminal issue the command.

```shell
> git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   README.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	docs/
	mkdocs.yml

no changes added to commit (use "git add" and/or "git commit -a")
```

This tells us on which branch our local repo is, which files have changed, and which files are new,
and therefor unknown to our git repo sofar. Files unknown to th git repo are called _untracked_.

!!! Note
    Which files are listed depends - obviously - on which files you modified since the last commit.
    When the project was created with `wip init ...` a first commit is automatically executed.
    Unless you explicitly requested no to create a remote repo, a push is also automatically
    executed.

!!! Tip
    It is useful to commit and push your work at every point where something was added and/or tested
    successfully.

!!! Tip
    If you are not the only developer on a project, or your project has many users, study the
    concept of [git branches](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell).

Untracked files must be added before you can store them in the git repo. Adding a directory 
automatically add all files in it:

```shell
> git add docs
> git status
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   docs/api-reference.md
	new file:   docs/index.md
	new file:   docs/overview.md

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   README.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	mkdocs.yml
```

The `docs/` files are now no longer untracked, but identified as _new_, but _to be committed_.

```shell
> git add mkdocs.yml
> git status
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   docs/api-reference.md
	new file:   docs/index.md
	new file:   docs/overview.md
	new file:   mkdocs.yml

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   README.md
```

The file `README.md` (_modified_) can be added too, to make it _to be committed_, but since it is
already known to the repo (_i.e._ the previous version is already in the local repo), we can commit
it right away using the `-a`flag. To store the _to be committed_ files in the local repo we thus use
the command:

```shell
> git commit -a -m "added documentation"
[main 11254ea] added documentation
 5 files changed, 57 insertions(+)
 create mode 100644 docs/api-reference.md
 create mode 100644 docs/index.md
 create mode 100644 docs/overview.md
 create mode 100644 mkdocs.yml
```

The `-a` flag tells git to add all _modified_ files _not staged for commit_ before actually
committing. the `-m "added documentation"` flag specifies the commit message. In the remote GitHub
repo each file will be labeled with the commit message of the latest commit in which the file was
changed.

When we ask for the status now, we see that there is nothing to commit, but that the local repo is
one commit ahead (that we just executed) of the remote repo `origin/main`. That means that the
changes of that last commit are in the local repo, but not yet in the remote GitHub repo.

```shell
> git status
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```

That is fixed by pushing:

```shell
> git push
Enumerating objects: 10, done.
Counting objects: 100% (10/10), done.
Delta compression using up to 8 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (8/8), 1.44 KiB | 736.00 KiB/s, done.
Total 8 (delta 1), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/etijskens/Dot.git
   2024c98..11254ea  main -> main
```

```shell   
> git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```
