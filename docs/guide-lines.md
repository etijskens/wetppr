# Assignment guide lines

!!! note 
    This is work in progress ...

The [assignment](assignment.md) is there because programming is something you can only learn by doing. It involves 
 important skills that you should develop while working on the assignment:

- Understand the math of the problem and the algorithm to solve it,
- Do research on the problem, with respect to solution algorithms and implementation issues.
- Understand the working of a computer and a supercomputer.
- Reason about the implementation of the algorithm.
- Write and debug code in Python. 
- Learn how slow functions can be sped up by converting them to either C++ or Fortran. 
- Run your code on one of the UAntwerp HPC clusters.

Learning is an incremental process. Especially for scientific software development the following is a good approach:

1. Try, and test (We'll see what testing exactly means). 
2. Fail (often, [the faster you fail, the faster you learn](https://testsigma.com/blog/test-automation-achieve-fail-fast-fail-often/)! ).  
3. Think and do research (*Google* - or any other good search engine, for that matter - is your best friend), and come 
   up with an improvement. This is the hardest part, it requires intelligence and creativity.
4. Iterate, *i.e.* restart at 1., until you no more fail and are satisfied with the solution.
5. Document your itinerary. Especially, keep track of the documents that guided you to a satisfactory solution.

Although this approach may look as if you are supposed to find the solution to the problem in books or on the *World 
Wide Web*, this does not at all exclude creativity. Learning about how other researchers approached a problem, can 
easily spark new ideas that get you going. The *fail fast, fail often* principle also ***urges you to start as simple 
as possible*** and ***make incremental changes***. Don't write a lot of code before you try and test. Typically,  
and this is corroborated by research, one bug is introduced with every new 10 lines. Finding 10 bugs in 100 lines is 
a lot more difficult than finding one bug in 10 lines (although sometimes there is more than one bug :( ). 

A PhD student once asked me for support. He had written a 10 000 line Fortran program
(without tests). When he ran it, the results were not what he expected and he suspected that there was a bug 
'somewhere'. He asked if I could help him find the bug and - no kidding - by the end of next week because the 
program had to go into production by then. I had to disappoint him and told him that he needed a true magician, 
which I am not. Obviously, the program was flawed in some sense, but other than a bug it might just as well be:

- The program contains many bugs, which is very well possible in view of its size.
- The algorithm for solving the problem is inappropriate.
- There is an accuracy problem, related e.g. discretisation of time, space, or a insufficient basis function for 
  expanding the solution, or related to the finite precision of floating point numbers. (Floating point numbers are a 
  processor's approximation of the real numbers, but they do have different mathematical properties. *E.g.* floating 
  point addition is **not** commutative.)
- The mathematical formulation itself could be flawed or misunderstood.
- It is even possible that the program is correct but that the researchers expectations are wrong. 
- ...

It could easily take weeks, if not months to write tests for the individual components to learn about the behaviour 
of the program and narrow down to the source of the error. 

For this reason a sound strategy for scientific software development that makes sure that the code you write has a 
sense of correctness is indispensable. Had the researcher come to me before he started programming this is the 
advice he would have been given: 

!!! note "Advice"
    ***Write 5 lines of code and test them before you proceed (with the next 5 lines)***. Just 5, not 10! Your test 
    code is also code and will initially contain bugs as well. As you get more experienced you may increase that 
    number  to 6, even 7, ...  

Admittedly, this advice is slightly biased on the conservative side, but I hope you get the point. You will be 
surprised how many mistakes you make, being a novice. But as you will discover the source of error soon, your 
progress will not come to halt. Instead you will learn fast and your progress will even speed up. I will give you 
practical tools to accomplish this. 