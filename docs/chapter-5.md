# Chapter 5 - A strategy for the development research software

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
experience that we build up. They enable us to proceed faster when pieces of a last year's problem may be useful today. 

None of these features come without effort. They comprise a learning process, require attention and research. 
You build experience an building on experience. 

Here is a story that demonstrates an anti-pattern for research code development. 

!!! note
    The term **pattern** refers to a set problems with common features that can be efficiently solved with the same 
    approach, by applying the pattern. The term comes from a very useful 
    [book](https://springframework.guru/gang-of-four-design-patterns/) "Design Patterns - Elements of reusable 
    object-oriented software", by Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, 1995. Several 
    "pattern" books later transferred the approach to other domains. 
    
    An **anti-pattern** is a pattern that perhaps solves the problem, or not, but if it does, in pessimal way. It is a 
    pattern NOT to follow.

A PhD student once asked me for support. He had written a 10 000 line Fortran program  When he ran it, the results 
were not what he expected, and he suspected that there was a bug 'somewhere'. He asked if I could help him find the 
bug and - no kidding - by the end of next week because the program had to go into production by then. I had to 
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
- It is even possible that the program is correct but that the researchers expectations are wrong. 
- ...

It could easily take weeks, if not months to write tests for the individual components to learn about the behaviour 
of the program and narrow down to the source of the error. 

For this reason a sound strategy that makes sure that the code you write is correct, that does what you want, and 
builds understanding of the problem at hand as you proceed, is indispensable. 


