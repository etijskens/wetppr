[//]: # (code below is for allowing for MathJax rendering of LateX expressions)

<script type="text/javascript"
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS_CHTML">
</script>
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {
      inlineMath: [['$','$'], ['\\(','\\)']],
      processEscapes: true},
      jax: ["input/TeX","input/MathML","input/AsciiMath","output/CommonHTML"],
      extensions: ["tex2jax.js","mml2jax.js","asciimath2jax.js","MathMenu.js","MathZoom.js","AssistiveMML.js", "[Contrib]/a11y/accessibility-menu.js"],
      TeX: {
      extensions: ["AMSmath.js","AMSsymbols.js","noErrors.js","noUndefined.js"],
      equationNumbers: {
      autoNumber: "AMS"
      }
    }
  });
</script>

# Chapter I

!!! note
    This is work in progress. It is incomplete, unfinished and flawed, just as life. However, sometimes *good enough is
    good enough*, and it will improve with time. 

Material:

- this text and
- [this presentation](presentations/lecture-1.pptx).

## Overview

- What is a parallel program?
- Possible reasons to parallelize a program.
- When to parallalize a program, and what to do first ...
- Common approaches towards parallelization
- Case study from Molecular Dynamics
- Final remarks

## What is a parallel program?

A parallel program is a program that distributes its work over different processing units such that parts of its 
work load can be computed simultaneously. At the end the program gathers the partial results from the processing 
units and combines them in a global result. If the tasks are independent of each other, the program is called 
**embarrassingly parallel**. In general, the individual tasks are not independent and need to exchange information. 
This is called **communication**. The opposite of a parallel program is a **serial** or **sequential** program, 
executing all its instructions one after the other. 

## Possible reasons to parallelize a program

### 1. Reduce the time to solution

The term **time to solution** in general means the time your machine needs to solve a computational problem. If the 
problem can be divided in smaller tasks that can be computed simultaneously, the time to solution decreases. If a 
company can solve a research or engineering question in a week or a day, that is an important difference. A 
processing unit has a maximum number of instructions it can execute per second, this is called its **peak 
performance**. Obviously, the peak performance is a machine limit puts a hard limit to what a processing unit can 
achieve in a given amount of time. But instructions operate on data, and moving data from main memory takes time as 
well. A program that must process lots of data but does little computation is limited by the speed at which the 
processing unit can fetch data from the main memory. This is called the **memory bandwidth** (usually in Mbits/s).
Programs that do a lot of computation and does not move a lot of data in or out of main memory is called **compute 
limited**. A program that moves a lot of data and little computation is **bandwidth limited**. While in the past 
programs used to be compute bound, today, most programs are memory bound, because the speed of the processing units 
increased much faster than the speed of memory. As a consequence, efficient memory access patterns are crucial to the 
performance of a program.  

### 2. Solve bigger problems in the same time

There is a third machine limit that plays a role, namely the amount of main memory. This puts a limit on the size of 
the problem that can be treated, e.g. the number of volume elements in a CFD simulation or the number of atoms in a 
MD simulation. If the program can distribute the work over, say 10 machines, it has 10 times the amount of memory at 
its disposition and thus can solve a 10 times bigger problem.  

### 3. Produce more accurate solutions

More accuracy can come from more complex physical models, or from using more basis functions to expand the solution.
This leads to more computation and perhaps a prohibitively long time to solution. Problems involving discretisation 
(the process of dividing the domain of a computational problem in small elements, as in computational fluid dynamics 
and finite element modelling) the accuracy typically improves when the elements get smaller, as in approximating the 
integral under a curve by rectangles. In both cases parallelization of the program may be necessary to obtain a 
solution. 

### 4 Competition

If a program that is in competition with other programs that solve the same problem, parallelization will allow it 
to reduce the time to solution, to compute bigger problems and achieve more accurate solution. This is, obviously, a 
competitive advantage.  

### Can't I just by a faster and bigger computer?

Nope, that fairy tale ended approximately at the beginning of this century with the advent of the multi-processor 
computer. Increasing the peak performance by increasing the clock frequency was no longer possible, because the 
power consumption of a processor increases as the third power of the clock frequency. At a certain point it became 
impossible or too expensive to cool the processor. The only way to get a processor execute more instructions per 
second was to put more processing units on it (cores). At that point serial program became even slower on the new 
multi-processors because the clock frequency was reduced to remain inside the power envelope. Moore's law predicts 
that the number of transistors in a processor doubles every 18 months due to increasing miniaturization. With this the  
combined peak performance of the multi-processors increases as well, but the peak performance of the individual 
processing units no longer does. This makes it necessary to parallelize programs in order to keep up with Moore's 
law. It must be said that the increase of peak performance was not always in line with Moore's law. At some point 
the peak performance of processing units was increased by adding parallelization concept in single processing units 
like pipelining and SIMD vectorisation. We'll come to that later.

### When to parallelize, and what to do first ...

When your program takes too long, the memory of your machine is too small for your problem or the accuracy you need 
cannot be met, you're hitting the wall. Parallelization seems necessary, and you feel in need of a supercomputer.
However, supercomputers are expensive machines and resources are limited. It should come to no surprise that it is 
expected that programs are allowed to run on supercomputers only if they make efficient use of their resources. 
Often, serial programs provide possibilities to improve the performance. These come in two categories:

#### common sense optimisations

Common sense optimizations come from a good understanding of the mathematical formulation of the problem and seeing 
opportunities to reduce the amount of work. We give two examples. 

##### 1. Magnetization of bulk ferromagnets

I was asked to speed up a program for computing the magnetisation $m(T)$ of bulk ferromagnets as a function of 
temperature $T$. This is given by a self-consistent solution of the equations:

$$ m = \frac{1}{2 + 4\Phi(m)} $$

$$ \Phi(m) = \frac{1}{N} \sum_{\textbf{k}} \frac{1}{e^{\beta\eta(\textbf{k})m} - 1} $$

with $ \beta = 1/{k_B T} $. At $T=0$ we have $m(0) = m_0 = 0.5$, and at high $T$, $m(T)$ approaches zero.

The solution is a curve like this:

![m(T)](/public/m(T).png)

The program compute this as follows: For any temperature $T$, set $m = m_0$ as an inital guess. Then iterate $ m_
{i+1} = 1/(2 + 4\Phi(m_i)) $ until $ \Delta m = m_{i+1} - m_i $ is small. Here,

$$ \Phi(m) = \sum_{n=1}^\infty \frac{a}{\pi} \left(\int_0^{\pi/a} dq e^{-nm\beta\eta_1(q)}\right)^3 $$

and the integral is computed using Gauss-Legendre integration on 64 points.  

Experimenting a bit with this formula one easily notices that for every $T$ the iterative procedure starts out more 
or less the same, as they all have the same initial guess. However, if we compute tempurature points at equidistant 
tempuratures, *e.g.* $T_j = \delta j$ for some $\delta$ and $j=0,1,2, ...$ we can use $m_j$ as an initial guess 
instead of $m_0$. This turns out to be 1.4x faster. Not a lot but that inspired us further improve the initial guess 
using linear interpolation of $m_j$ from $m_{j-1}$ and $m_{j-2}$ leading to a speedup of 1.94x. Finally, fixing the 
initial guess by quadratic interpolation from  $m_{j-1}$, $m_{j-2}$ and $m_{j-3}$ the code speed up by a factor 2.4 
and that without acttually modifying the code. This optimisation comes entirely from understanding what your 
algorithm actually does. Investigation of the code itself demonstrated that it made suffered from a lot of dynamic 
memory management and that it did not vectorize. After fixing these issues, the code ran an additional 13.6x faster. 
In total the code was sped up by an impressive 32.6x.

##### Transforming the problem domain 

At another occasion I had to investigate a code for calculating a complicated sum of integrals in real space. After 
fixing some bugs and some optimisation to improve the efficiency, it was still rather slow because the formula 
converged slowly  As the code was running almost at peak performance, so there was little room for improvement. 
However, at some point we tried to apply the Fourier transform to get an expression in frequency space. This 
expression turned out to converge much faster and consequently far less terms had to be computed, yielding a speedup 
of almost 2 orders of magnitude and was much more accurate. This is another example of common sense optimisation 
originating in a good mathematical background. The natural formulation of a problem is not necessarily the best to 
use for computation.    

!!! note
    unfinished ...