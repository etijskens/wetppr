# Evaluation of this course

In this course you will be learning by doing. You will be given an assignment, a (parallel) programming task on which you will work for several weeks, under my supervision and with my support. 

The exam consists of a presentation of your project work (usually in the last week of the course) in which you must

- explain the problems you encountered,

- explain your approach,

- provide performance measurements for the different versions your code, and for different node counts,

- explain the performance measurements,

- tell me what you found difficult during this course.

During the presentation I will ask some questions, mainly because I am curious and eager to learn something, but also to ensure that you understand what you present.

## Assignment

Here is this year's [assignment](assignment-2023-24.md).

## Use of VSC clusters for the assignment

Students of the course 2000wetppr must use one of the VSC-clusters for the project work. Check out [Access to VSC infrastructure and set up of your environment](vsc-infrastructure.md). 

## Guide lines

### Mandatory tools to be used

You ***MUST*** (!)

- create your exercise projects with the wiptools CLI (`wip`),

- deliver your exercise projects on your GitHub account.

If not, you will not receive any credits.

#### Use git

Git is a version control system. It helps you storing versions of your projects. As a novice in programming, git helps you 

* To ensure that you do not loose your programming work by providing a versioned backup.

* To store the history of your project. If at any time you might decide that the current version of your project is on the wrong track, you can always return to previous versions, even on a file level.

* To easily transfer your project to another machine. You may be working on your project on your laptop, a desktop at home, one of the VSC clusters, ... without problems. It also provides a clean way of delivering over your programming assignments to the evaluator and asking for help to fix bugs and review code. Therefor, ***using git is mandatory*** for this course. 

If you become a researcher later, you will learn that git also helps you 

* To collaborate with other people on a piece of software.

* To separate released work from development and bug fixing.

#### Git workflow

Below we focuses on a git work flow useful for the programming projects for the evaluation of this course.

Git stores the different versions of your project in a **local git repository**. This is a `.git` directory in your project directory. Obviously, this local repository is only accessible from your machine. To make it accessible to others, you also need a remote **GitHub repository**. This is located in the cloud `https://github.com/<your-GitHub-username>/<your-project-name>`. To transfer changes to your project files to the repositories this workflow is appropriate:

1. List your changes using the `git status` command.

2. Stage changed files that you want to transfer to the local git repository with the `git add <file-to-stage>`. The `git status` command shows which changes are staged and which are not.

3. Transfer staged changes to the local git repository using the `git commit` command. (This called _committing changes_). The `git commit` command will prompt you for a commit message. Here's a single page of [good advice on committing changes](https://tilburgsciencehub.com/building-blocks/collaborate-and-share-your-work/use-github/git-commits/). 

    !!! Tip "Committing incomplete changes"
        Best practises on commiting recommends that you should _only_ commit completed changes. Sometimes you simply want to store the current status just for backup (_e.g._ you want to continue working from home the next day on your home computer). In that case use a commit message that makes clear that this is a commit with incompleted changes, _e.g._ "Work in progress - incomplete changes!". Use exactly the same message every time you do this.

4. Transfer your changes from the local git repository to the remote repository at github.com using the `git push` command.

5. To transfer a remote Github repository to a local machine that does not yet have a local repository for that project, use the command `git clone §https://github.com/<your-GitHub-username>/<your-project-name>`.

6. To transfer the latest changes from a remote Github repository to a local machine that already has local repository for that project, use the command `git pull`.

What has not yet been described in this work flow is how you start. How do you create a local git repository? How do you create a remote GitHub repository? How do you connect one to the other? This is taken care of by another tool that is ***mandatory*** for students of this course: [wiptools](https://etijskens.github.io/wiptools/). 

#### Use wiptools

[Wiptools](https://etijskens.github.io/wiptools) is a Python package and a CLI for Python project management. It was developed to assist in research software development along the strategy described in [Chapter 5][a-strategy-for-the-development-research-software]. When creating a new project with the wip CLI:

```shell
> cd workspace
> wip init foo
...
```

a set of templates is used to create a Python project `foo` with directories for tests and documentation, a local git repository and a remote GitHub repository `https://github.com/<your-github-username>/foo`. On top of that you can add

- Python sub-modules,

- binary extension modules built from C++ or Modern Fortran source,

- CLIs and CLIs with subcommands.

All files created are automatically committed and pushed to the remote GitHub repository. After this, the [Git workflow][git-workflow] above can be applied easily.

Wiptools is suitable for small projects but scales very well to large projects.

### Learning by doing

The assignment is there because imho ***programming is something you can only learn by doing***. It involves important skills that you should develop while working on the assignment:

- Use the background information presented in chapters 1-4 and carefully read chapter 5 on research strategy.

- Reason about the mathematical formulation of the problem and the algorithm to solve it,

- Do research on the problem, with respect to solution algorithms and implementation issues.

- Write and debug code in Python.

- Learn how slow Python functions can be sped up by converting them to either C++ or Fortran.

- First develop code on your local machine. In general, local development and debugging are more user friendly.

- Once things work, migrate your code for further testing to one of the UAntwerp HPC clusters.

Learning is an incremental process. Especially for scientific software development the following is a good approach:

1. ***Try, and test*** (We'll see what testing exactly means).

2. ***Fail*** (often, [the faster you fail, the faster you learn](https://testsigma.com/blog/test-automation-achieve-fail-fast-fail-often/)! ).

3. ***Think and do research*** (*Google* - or any other good search engine, for that matter - is your best friend), and come up with an improvement. This is the hardest part, it requires intelligence and creativity.

4. ***Iterate***, *i.e.* restart at 1., until you no more fail and are satisfied with the solution.

5. ***Document your itinerary***. Document your classes, functions, variables, and keep track of the documents that guided you to solving the problems encountered. When you will look at your work three months (only!) after you left it as is, you will wonder what it was all about if you didn't document it.

Although this approach may look as if you are supposed to find the solution to the problem in books or on the *World Wide Web*, this does not at all exclude creativity. Learning about how other researchers approached a problem, can easily spark new ideas that get you going. The *fail fast, fail often* principle also

- ***urges you to start as simple and small as possible*** and

- ***make incremental changes***.

Don't write a lot of code before you try and test. Typically, and this is corroborated by research, one bug is introduced with every new 10 lines. Finding 10 bugs in 100 lines is a lot more difficult than finding one bug in 10 lines (although sometimes there is more than one bug :( ).

!!! Tip
    ***Write 5 lines of code and write a test for them. Do not proceed (with the next 5 lines) before the test passes***. Just 5, not 10! Your test code is also code and will initially contain bugs as well. ***As you get more experienced you may increase that number to 6, even 7, ...***

Admittedly, this advice is slightly biased to the conservative side, but I hope you get the point. You will be surprised how many mistakes you make, being a novice. But as you will discover the source of error soon, your progress will not come to a halt. Instead, you will learn fast and your progress will even speed up. You will be given practical tools to accomplish this.

!!! note "Caveat"
    There is a small disadvantage to the approach we are following. It is biased towards **bottom-up design**. In bottom-up design your start from the details, gradually aggregating them into larger parts, and, eventually, into the final application. Its opponent is **top-down** design, in which you start with the a high-level formulation of the problem. This is then broken down in smaller components and gradually refined until all details are covered. With a bit of imagination it is, however, possible to write tests for a top-down approach by focussing on how the components work together, rather than on what they are doing. Top-down design is important because it forces you to think on the high-level structure of your application. This is paramount to how fast users will adopt your application, because it relates to user-friendly-ness, intuitive understanding, flexibility, ... In general, however, research scientists seem to more at ease with bottom-up thinking.
