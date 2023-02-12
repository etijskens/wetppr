# Evaluation

In this course you learning by doing. You will be given an assignment, a (parallel) programming task on which you 
will work for several weeks. At our final session you will give a presentation about your work

- explaining the problems you encountered,
- explaining your approach,
- providing performance measurements for the different versions your code, and for different node counts,
- explaining the performance measurements,
- explaining what you found difficult during this course.

Here are some important skills that you should develop during this course:

- understand the math of the problem and the algorithm to solve it,
- reason about the implementation of the algorithm,
- 

Learning is an incremental process. Especially for scientific software development the following is a good approach:

1. Try, and test (We'll see what testing exactly means). 
2. Fail (often, [the faster you fail, the faster you learn](https://testsigma.com/blog/test-automation-achieve-fail-fast-fail-often/)! ).  
3. Think and do research (*Google* - or any other good search engine, for that matter - is your best friend), and come 
   up with an improvement. This is the hardest part, it requires intelligence and creativity.
4. Iterate, *i.e.* restart at 1., until you no more fail and are satisfied with the solution.
5. Document your itinerary. Especially, keep track of the documents that guided you to a satisfactory solution.

Although this approach may look as if you are supposed to find the solution to the problem in books or on the *World 
Wide Web*, this does not at all exclude creativity at all. Learning about how other researchers approached a problem,
can easily spark new ideas that get you going. The *fail fast, fail often* principle also **urges you to start as 
simple as possible**. Don't write a lot of code before you try and test. Typically, there's a bug in every 10 lines. 
Finding 10 bugs in 100 lines is a lot more difficult than finding one bug in 10 lines (although sometimes there is 
more than one bug :( ). A PhD student once asked me for support. He had written a 10 000 line Fortran program, 
without tests. The results were not what he expected: "If I could help him to find the bug, by the end of next week, 
it must go in production then. I had to disappoint him, told him to look out for a true magician, which I am not. 
Obviously, the program was flawed in some sense, but other than a bug it might as well be:

- a bad algorithm for solving the problem,
- an accuracy problem, related e.g. discretisation of time, space, or a insufficient basis function for expanding 
  the solution, 
- even the mathematical formulation itself could be flawed or misunderstood,
- ...

So, stick to this advice: 

!!! note "Advice"
    **Write 5 lines of code and test them**. Only 5, not 10! Your test code is also code and will initially contain 
    bugs as well. As you get more experienced you may increase that number  to 6, even 7, ... Ok, you get the point. 

I assure you that, not only your progress will be faster, you'll learn faster too, which makes you progress even 
faster. 