# Chapter 5 - A strategy for the development research software

## The need of a strategy for the development research software

You are facing a new research question, to be solved computationally and on your shelf of computational tools nothing 
useful is found. You start with an empty sheet of paper on you desk. or rather with an empty screen on your laptop. 
How you take on such a challenge? This chapter is about a strategy for (research) code development that

1. minimizes coding efforts, 
2. allows for high performance, 
3. provides flexible and reusable software components.

_Coding efforts_ is more than just the time to type your program in an editor or IDE. It is also the time you spend 
making sure that your code is correct, and stays correct while you are working on it, restructuring its components, 
ensuring that it solves the problem you need to solve.

High performance is essential when we run our problem on a supercomputer, but perhaps that is not necessary. We want 
to postpone performance optimisation until it is really needed. This principle was set in stone in a quote by Donald 
Knuth in 1974 already: "Premature optimisation is the root of all evil". Spending time on optimisation before it is 
needed is wasting time, and stopping progress. Initially, we want to focus on simplicity and correctness, and on 
understanding  the characteristics of the problem at hand. If the algorithm we choose to solve is inadequate, we 
want to know that as soon as possible. On the other hand, when it is needed, we want our project to be in a state 
that facilitates performance optimisation where it is needed.  

Finally, we want an approach that builds experience. Flexible and reusable software components are materializing the 
experience that we build up. They enable us to proceed faster when pieces of a last year's problem may be useful 
today. Two important aspects of reusable code are writing simple functions and classes with a single functionality, 
and documentation. Well documenting your code increases the chance that when you check out your code three months 
later, you will not be staring baffled at your screen wondering what it was all about. It happens to me, it can 
certainly happen to you. 

None of these features come without effort. It is also not a bucket list of checkboxes to make sure that you did 
not overlook something. ***They comprise a learning process, require attention, disipline and research***. 

Here is a story that demonstrates an anti-pattern for research code development. 

!!! note
    The term **pattern** refers to a set problems with common features that can be efficiently solved with the same 
    approach, by applying the pattern. The term comes from a very useful 
    [book](https://springframework.guru/gang-of-four-design-patterns/) "Design Patterns - Elements of reusable 
    object-oriented software", by Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, 1995. Several 
    "pattern" books later transferred the approach to other domains. 
    
    An **anti-pattern** is a pattern that perhaps solves the problem, or not, but if it does, in pessimal way. It is a 
    pattern NOT to follow.

A PhD student once asked me for support. He had written a 10 000 line Fortran program. When he ran it, the results 
were not what he expected, and he suspected that there was a bug 'somewhere'. He asked if I could help him find the 
bug and - no kidding - by the end of next week, because the program had to go into production by then. I had to 
disappoint him and told him that he needed a 'true' magician, which I, unfortunately, was not. Obviously, the program 
was flawed in some sense, but other than a bug it might just as well be one or more of the situations below:

- The program may contain many bugs, which is very well possible in view of its size. On average a programmer 
  introduces about 1 bug in every 10 lines of code! Check this link for [some amazing facts](https://www.
  openrefactory.com/intelligent-code-repair-icr/) 
- The algorithm for solving the problem is inappropriate. 
- There is an accuracy problem, related e.g. discretisation of time, space, or a insufficient basis function for 
  expanding the solution, or related to the finite precision of floating point numbers. (Floating point numbers are a 
  processor's approximation of the real numbers, but they do have different mathematical properties. *E.g.* floating 
  point addition is ***not*** commutative.)
- The mathematical formulation itself could be flawed or misunderstood.
- The program is correct, but the researchers expectations are wrong. 
- ...

It could easily take weeks, if not months to write tests for the individual components to learn about the behaviour 
of the program and narrow down to the source of the error. This anti-pattern is a disaster waiting to happy.

For this reason a sound strategy that makes sure that the code you write is correct, that does what you want, and 
builds understanding of the problem at hand as you proceed, is indispensable. The strategy proposed below has been 
shaped by a lifetime of research software developement. I use it in nearly every software project I take on, whether 
it is small or big, simple or complex, starting from scratch or from someone else code. 

The proposed strategy builds on five principles:

1. Start out in a high level programming language. [Python](https://www.python.org) is an excellent choice.
2. Start out simple, as simple as possible, in order to build up understanding of your problem and how it should 
   be solved fast. 
3. Test and validate your code, continuously, and for small code fragments, to discover bug and mistakes as soon as 
   possible. 
4. Improve your code, adding better algorithms (which usually are more complex), pay attention to data structure 
   facilitating good data access patterns, think of [common sense optimisations][common-sense-optimisations], 
   gradually increase the complexity of the problem.  
   Keep principle 3. in mind and continue testing and validating the improvements.
5. If neccessary, optimise your code. Necessary is when the time to solution is too long.
6. If necessary, parallelise your code. Necessary is when the time to solution is still too long after paying 
   attention to principle 5., or if the problem does not fit in the memory of a single machine. In that case it it 
   advisable to optimise anyway to not waste cycles on an expensive supercomputer. 

!!! tip "Tip for researchers of the University of Antwerp and institutes affiliated with the [VSC](https://www.vscentrum.be)"
    Researcher of the University of Antwerp and institutes affiliated with the [VSC](https://www.vscentrum.be) are 
    wellcome to contact me for support when developing research software. The best time to do that would be before 
    having written any line of code at all for the problem, in order to follow all principles.    

Below, we explain these principles in depth.

## Principle 1. Start out in a high level language

[Python](https://www.python.org) is an excellent choice:

- [Python](https://docs.python.org/3/) is a 
  [high-level general-purpose programming language](https://docs.python.org/3/faq/general.html#what-is-python-good-for) 
  that can be applied to many different classes of problems. 
- Python is easy to learn. It is an interpreted and interactive language and programming in Python is intuitive, 
  producing very readable code, and typically significantly more productive than in low-level languages as 
  C/C++/Fortran. Scripting provides a very flexible approach to formulating a research problem, as compared to an 
  input file of a low-level language program. 
- It comes with a [large standard Library](https://docs.python.org/3/library/index.html#library-index)
- There is wide variety of third-party extensions, the [Python Package Index(PyPI)](https://pypi.org). Many packages 
  are built with HPC in mind, on top of high quality HPC libraries. 
- The functionality of standard library and extension packages is enabled easily as `import module_name`, and 
  installing packages is as easy as: `pip install numpy`. The use of modules is so practical and natural to Python 
  that researchers do not so often feel the need to reinvent wheels.
- Availability of High quality Python distributions (
  [Intel](https://www.intel.com/content/www/us/en/developer/articles/technical/get-started-with-intel-distribution
  -for-python.html), [Anaconda](https://www.anaconda.com/products/distribution)), cross-platform Windows/Linux/MACOS
- Python is open source. In itself that is not necessarily an advantage, but its large community guarantees an 
  very good documentation, and for many problems high-quality solutions are found readily on user forums.  
- Python is used in probably any scientific domain, and may have many third party extension freely available in that 
  domain. It is available with a lot scientific Python packages on all [VSC](https://www.vscentrum.be)-clusters.
- Several high-quality Integrated Development Environments (IDEs) are freely available for Python: _e.g._ 
  [PyCharm](https://www.jetbrains.com/pycharm/), [VS Code](https://code.visualstudio.com), which at the same time 
  provide support for C/C++/Fortran.
- Although Python in itself is a rather slow language, as we will see, there are many ways to cope with performance 
  bottlenecks in Python. 
  
In many ways, Python gently pushes you in the right direction, providing a pleasant programming experience.

![excellent-just-ahead](public/excellence-just-ahead.png)

As an alternative on could consider [Julia](https://julialang.org). Following a different programming paradigm, called 
[multiple dispatch](https://docs.julialang.org/en/v1/manual/methods/), its learning curve is probably a bit steeper 
and it has a smaller community. However, it is more performant than Python. On the other hand its programming 
productivity might not be that of Python. 

An other alternative could be [Matlab](https://www.mathworks.com/products/matlab.html). Although it has a long 
history of scientific computing, from as a language is it not as well designed as Python, and it is not fit for HPC. 
Moreover, it is a commercial product, and the community using it is not as willing to share its solutions as for 
Python, and there are much less extensions available. Often, you will need to solve the problem yourself, and, as a 
consequence, proceed at a slower pace.

Starting out in a low-level programming language (C/C++/Fortran) is certainly a bad idea. Even if you are an 
experienced programmer you will proceed slower. The productivity of Python is easily 10 times larger than for 
C/C++/Fortran because:

- the advantages coming with an interpreted language, _vs._ a compiled language,
- the fact that Python is a very well designed, expressive and readable language with a rather flat learning curve,
- the availability of a large standard library and a wide range of domain-specific third party extensions, as well 
  as the ease with which these are enabled in your code.

Hence, this course sticks to Python. 

## Principle 2. Start out as simple as possible

Take a small toy problem, the smallest you can think of that still represents the problem that you want to 
solve. There is a famous quote, attributed to Einstein 
([although it seems he formulated it differently](https://skeptics.stackexchange.com/questions/34599/did-albert-einstein-say-make-everything-as-simple-as-possible-but-not-simpler))
"Make everything as simple as possible, but not simpler". That applies very well here. Ideally, take a problem with 
a known analytical solution. Look for something you can easily visualise. Four atoms are easier to visualise than a 
hundred. Visualisation is an perfect way for obtaining insight (pun intended!) in your problem. Choose the simplest 
algorithm that will do the trick, don't bother about performance. Once it works correctly, use it as a reference 
case for validating improvements.  

## Principle 3. Test and validate

In view of [these amazing facts](https://www.openrefactory.com/intelligent-code-repair-icr/) There seems to be 
little chance that a programmer writes 100 lines of code without bugs. On average there should be 7 bugs in every 
100 lines. Probably not all these bugs affect the outcome of the program, but in research code the outcome is of 
course crucial. How can we ensure that our code is correct, and remains so as we continue to work on it? The anwer 
is unit-tests. [Unit-testing](https://en.wikipedia.org/wiki/Unit_testing) are pieces of test-code together with 
verified outcomes. In view of the abundancy of bus it is best to test small pieces of code, in the order of 10 lines.
Test code is also code and thus can contain bugs as well. The amount of test code for a system can be large. An 
example is probaly the best way to demonstrate the concept. In chapter 4 we discussed the case study 
[Monte Carlo ground state energy calculation of a small atom cluster][monte-carlo-ground-state-energy-calculation-of-a-small-atom-cluster]
and a small project [wetppr/mcgse][project-mcgse] where the original study is repeated with a Morse potential, 
described by the formula:

$$ V(r) = D_e(1 - e^{-\alpha(r-r_e)})^2 $$

The code for this function is found in [wetppr/mcgse/__init__.py](public/symlinks/__init__.py). Note that we 
provided default unit values for all the parameters: 

```python
import numpy as np

def morse_potential(r: float, D_e: float = 1, alpha: float = 1, r_e: float = 1) -> float:
	"""Compute the Morse potential for interatomic distance r.

	This is better than it looks, we can pass a numpy array for r, and it will
	use numpy array arithmetic to evaluate the expression for the array.
	
	Args:
		r: interatomic distance
		D_e: depth of the potential well, default = 1
		alpha: width of the potential well, default = 1
		r_e: location of the potential well, default = 1
	"""
	return D_e * (1 - np.exp(-alpha*(r - r_e)))**2
```
The implementation of the function comprises only one line. How can we test its correctness? One approach would be 
to list a few r-values for which we know the outcome. _E.g._ $V(r_e) = 0$. Here is a test funtion for it. Note that 

```python
from math import isclose

def test_morse_potential_at_r_e():
    # the value at r_e=1 is 0
    r = 1
    Vr = mcgse.morse_potential(x)
    Vr_expected = 0
    assert isclose(Vr, Vr_expected, rel_tol=1e-15)
```

Because the function is using floating point arithmetic, the outcome could be subject to roundoff error. We account 
for a relative error of `1e-15`. When running the test, an AssertionError will be raised whenever the relative 
error is larger than `1e-15`. Note that the test function's name starts with `test`. That allows an automated test 
runner as, _e.g._ [pytest](https://docs.pytest.org/en/7.2.x/) can discover the test function automatically. 

When it comes to testing functions it is practical to focus on mathematical properties of the function (fixing 
parameters to unity). _E.g._

- $0 \le V(r) $ for $r \in ]0,1]$,
- $0 \le V(r) < 1 $ for $r \in [1,+\infty[$,
- $V(r)$ is monotonously decreasing on $]0,1]$, 
- $V(r)$ is monotonously increasing on $[1,+\infty[$, 
- $V''(r)$ is positive on $]0,1]$,
- $V''(r)$ is positive on $]1,r_i]$, $r_i=1 - \log(1/2)$ being the inflection point,
- $V''(r)$ is negative on $]r_i, +\infty[$,
- ...

See `tests/wetppr/mcgse/test_mcgse.py` for details. The file contains many more tests for other functions in the file 
`wetppr/mcgse/__init__.py`. All tests are automatically run from the project directory `wetppr` with the command:

```bash
> pytest tests
==================================== test session starts =====================================
platform darwin -- Python 3.9.5, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
rootdir: /Users/etijskens/software/dev/workspace/wetppr
plugins: typeguard-2.13.3, mpi-0.5, anyio-3.6.2
collected 6 items

tests/wetppr/test_wetppr.py .                                                          [ 16%]
tests/wetppr/mcgse/test_mcgse.py .....                                                 [100%]

===================================== 6 passed in 1.65s ======================================
```
The command instructs pytest to check all `.py` files in or below the `tests` directory and look for methods with a 
name starting with `test` and execute them. As is clear from the output above it found 5 tests in 
`tests/wetppr/mcgse/test_mcgse.py`, all executed successfully. 

For every new method added to your code, add some tests and run `pytest`. For every code change run all tests again. 
Make sure they pass. 

## Principle 4. Improve 

## Principle 5. Optimise, if necessary 

## Principle 5. Parallelise, if necessary 
