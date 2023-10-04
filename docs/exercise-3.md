# Exercise 3 - The matrix-vector product

This exercise is evaluated.

It is mandatory to make use of `wip` for this exercise. Make sure

* that your worked is properly committed to your local git repo and pushed to your remote GitHub repo.
* that you give the evaluator read and write access to your project. (The write access is for
  feedback and for fixing problems).

## Preconditions

- You completed [Exercise 1 - Getting started with `wip`](exercise-1.md).
- You have prepared your personal environment on the Vaughan VSC cluster as described in
  [VSC infrastructure][vsc-infrastructure].

## Assignment

1. Construct a Python module with a method for the
[matrix-vector product](https://en.wikipedia.org/wiki/Matrix_multiplication) $y = Ax$,
$A_i = \sum_{j=1}^{n}{A_{ij}x_j}$. You can add the method to the Dot module package of
[Exercise 1 - Getting started with `wip`](exercise-1.md), or start a new `wip` package with the
command `wip init ...`. Start out with a Python implementation and use Numpy `array`s for
representing matrices and vectors throughout this exercise.

2. Time the implementation for square matrices ${n}\cross{n}$ of double precision elements Let $n$
   vary from 16, 32, 64, ... until the total amount of data exceeds the size of L3 cache (which may
   depend on the processor of your loocal machine). A double precision number takes 16 bytes.

3. Try improving the timings by using
   * @numba.jit
   * a C++ implementation
   * a Modern Fortran implementation

4. Compare your implementations with
   [numpy's own matrix-vector product](https://numpy.org/doc/stable/reference/generated/numpy.dot.html)
   `numpy.dot`.

5. Report all timings in the `README.md` file. Checkout [this link](https://www.markdownguide.org) for using MarkDown for simple
   text formatting.

6. Explain your observations with respect to the timings in the `README.md` file.
