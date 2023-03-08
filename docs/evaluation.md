# Evaluation of this course

In this course you will be learning by doing. You will be given an assignment, a (parallel) 
programming task on which you will work for several weeks, under my supervision and with my support. 

The exam consists of a presentation of your project work (usually in the last week of the course) in which you must

- explain the problems you encountered,
- explain your approach,
- provide performance measurements for the different versions your code, and for different node counts,
- explain the performance measurements,
- tell me what you found difficult during this course.

During the presentation I will ask some questions, mainly because I am curious and eager to learn something, but also 
to ensure that you understand what you present.

## Assignment

Here is this year's [assignment](assignment-2022-23.md).

## Use of VSC clusters for the assignment

Students of the course 2000wetppr must use one of the VSC-clusters for the project work. Check out [Access to VSC 
infrastructure and set up of your environment](vsc-infrastructure.md). 

## Guide lines

### Using a GitHub repo  
The code that you write must be regularly committed to a remote [GitHub](https://github) repository. This has many 
advantages:

- First, it serves as a backup. Every single commit can be retrieved at all times. So, you can't loose your code, 
  even not the older versions.
- Everyone with access to the repository can access the code. If you keep the repository public, that means everyone 
  with access to the internet. If you make it private, only the people you invite can access. 
- It is important that you give me access. If you have problems, I can clone your repository and debug it to see 
  what is going wrong,
- If you cooperate with another student on the project you can exchange updates easily. You can make use of git 
  branches to avoid bothering other people with your code changes before they are correct.  

The presentation of the project must be added to your GitHub repository before you present it. I will keep a copy of 
your project repo as a proof of your work.

### Learning by doing

The assignment is there because imho ***programming is something you can only learn by doing***. It involves 
important skills that you should develop while working on the assignment:

- Using the background information presented in chapters 1-4
- Reason about the mathematical formulation of the problem and the algorithm to solve it,
- Do research on the problem, with respect to solution algorithms and implementation issues.
- Write and debug code in Python. 
- Learn how slow Python functions can be sped up by converting them to either C++ or Fortran. 
- Run your code on one of the UAntwerp HPC clusters.

Learning is an incremental process. Especially for scientific software development the following is a good approach:

1. ***Try, and test*** (We'll see what testing exactly means). 
2. ***Fail*** (often, [the faster you fail, the faster you learn](https://testsigma.
   com/blog/test-automation-achieve-fail-fast-fail-often/)! ).   
3. ***Think and do research*** (*Google* - or any other good search engine, for that matter - is your best friend), and 
   come up with an improvement. This is the hardest part, it requires intelligence and creativity.
4. ***Iterate***, *i.e.* restart at 1., until you no more fail and are satisfied with the solution.
5. ***Document your itinerary***. Document your classes, functions, variables, and keep track of the documents 
   that guided you to solving the problems encountered. When you will look at your work three months (only!) after 
   you left it as is, you will wonder what it was all about if you didn't document it. 

Although this approach may look as if you are supposed to find the solution to the problem in books or on the *World 
Wide Web*, this does not at all exclude creativity. Learning about how other researchers approached a problem, can 
easily spark new ideas that get you going. The *fail fast, fail often* principle also 
 
- ***urges you to start as simple and small as possible*** and 
- ***make incremental changes***. 

Don't write a lot of code before you try and test. Typically, and this is corroborated by research, one bug is
introduced with every new 10 lines. Finding 10 bugs in 100 lines is a lot more difficult than finding one bug in 10 
lines (although sometimes there is more than one bug :( ). 

!!! Warning "Anecdotical evidence"
    A PhD student once asked me for support. He had written a ~10 000 line Fortran program
    (without tests). When he ran it, the results were not what he expected and he suspected that there was a bug 
    'somewhere'. He asked if I could help him find the bug and - no kidding - by the end of next week because the 
    program had to go into production by then. I had to disappoint him and told him that he needed a true magician, 
    which I am not. Obviously, the program was flawed in some sense, but other than _a_ bug it might just as well be 
    one or more of the issues below:

    - The program may contain many bugs, which is very well possible in view of its size.
    - The algorithm for solving the problem is inappropriate.
    - There is an accuracy problem, related to the discretisation of time, space, or an insufficient set of basis 
      functions for expanding the solution, or related to the finite precision of floating point numbers. (Floating 
      point numbers are a processor's approximation of the real numbers, but they do have different mathematical 
      properties. *E.g.* floating point addition is ***not*** commutative.)
    - The mathematical formulation itself could be flawed or misunderstood.
    - It is even possible that the program is correct but that the researcher's expectations are wrong. 
    - ...

    It could easily take weeks, if not months to write tests for the individual components to learn about the behaviour 
    of the program and narrow down to the source of the error. 

For this reason a sound strategy for scientific software development that makes sure that the code you write has a 
sense of correctness is indispensable. Had the researcher come to me before he started programming this is the 
advice he would have been given: 

!!! Tip
    ***Write 5 lines of code and write a test for them (the other way around is ok too). Do not proceed (with the 
    next 5 lines) before the test passes***. Just 5, not 10! Your test code is also code and will initially contain 
    bugs as well. ***As you get more experienced you may increase that number to 6, even 7, ...***

Admittedly, this advice is slightly biased to the conservative side, but I hope you get the point. You will be 
surprised how many mistakes you make, being a novice. But as you will discover the source of error soon, your 
progress will not come to a halt. Instead, you will learn fast and your progress will even speed up. I will give you 
practical tools to accomplish this. 