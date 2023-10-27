# Chapter 1 - Introduction

Material:

- this website

- which is built with `mkdocs` from [this GitHub repo](https://github.com/etijskens/wetppr/). The repo contains also example code, useful scripts, and code for some of the case studies of chapter 4.

- some presentations found [here](https://github.com/etijskens/wetppr/tree/main/docs/presentations). (Most of these need some reworking, especially those not in VSC format).

## Overview

- What is a parallel program?
- Possible reasons to parallelize a program.

## What is a parallel program?

A **parallel program** is a program that distributes its work over different processing units such that parts of its work load can be computed simultaneously. At the end the program gathers the partial results from the processing units and combines them in a global result. If the tasks areindependent of each other, the program is called **embarrassingly parallel**. In general, the individual tasks are not independent and need to exchange information. This is called **communication**. The opposite of a parallel program is a **serial** or **sequential** program, executing all its instructions one after the other. 

## Possible reasons to parallelize a program

### 1. Reduce the time to solution

The term **time to solution** in general is the time your machine needs to solve a computational problem. If the problem can be divided in smaller tasks that can be computed simultaneously, the time to solution decreases. If a company can solve a research or engineering question in a week or a day, that is an important difference. A processing unit has a maximum number of instructions it can execute per second, this is called its **peak performance**. Obviously, the peak performance is a machine limit puts a hard limit to what a processing unit can achieve in a given amount of time. But instructions operate on data, and moving data from main memory takes time as well. A program that must process lots of data but does little computation is limited by the speed at which the processing unit can fetch data from the main memory. This is called the **memory bandwidth** (usually in Mbits/s). Programs that do a lot of computation and does not move a lot of data in or out of main memory is called **compute limited**. A program that moves a lot of data and little computation is **bandwidth limited**. While in the past programs used to be compute bound, today, most programs are memory bound, because the speed of the processing units increased much faster than the speed of memory. As a consequence, efficient memory access patterns are crucial to the performance of a program.  

### 2. Solve bigger problems in the same time

There is a third machine limit that plays a role, namely the amount of main memory. This puts a limit on the size of the problem that can be treated, e.g. the number of volume elements in a CFD simulation or the number of atoms in a MD simulation. If the program can distribute the work over, say 10 machines, it has 10 times the amount of memory at its disposition and thus can solve a 10 times bigger problem.  

### 3. Produce more accurate solutions

More accuracy can come from more complex physical models, or from using more basis functions to expand the solution. This leads to more computation and perhaps a prohibitively long time to solution. Problems involving discretisation (the process of dividing the domain of a computational problem in small elements, as in computational fluid dynamics and finite element modelling) the accuracy typically improves when the elements get smaller, as in approximating the integral under a curve by rectangles. In both cases parallelization of the program may be necessary to obtain a solution. 

### 4 Competition

If a program that is in competition with other programs that solve the same problem, parallelization will allow it to reduce the time to solution, to compute bigger problems and achieve more accurate solution. This is, obviously, a competitive advantage.  

### Can't I just by a faster and bigger computer?

Regrettably not. That fairy tale ended approximately at the beginning of this century with the advent of the **multi-processor** computer, also called **multi-core** computer. Increasing the peak performance by increasing the clock frequency was no longer possible, because the power consumption of a processor increases as the third power of the clock frequency. At a certain point it became impossible or too expensive to cool the processor. The only way to get a processor execute more instructions per second was to put more processing units on it (cores). At that point serial program became even slower on the new multi-processors because the clock frequency was reduced to remain inside the power envelope. Moore's law predicts that the number of transistors in a processor doubles every 18 months due to increasing miniaturization. With this the combined peak performance of the multi-processors increases as well, but the peak performance of the individual processing units no longer does. This makes it necessary to parallelize programs in order to keep up with Moore's law. It must be said that the increase of peak performance was not always in line with Moore's law. At some point the peak performance of processing units was increased by adding parallelization concept in single processing units like pipelining and SIMD vectorisation. We'll come to that later.
