# Assignment 2022-23

## The Mandelbrot set

The **Mandelbrot set** $\mathcal{M}$ is defined as the set of all complex numbers $ c \in \mathbb{C} $, for which the 
iterative scheme 

$$ z_0 = 0 $$
$$ z_{i+1} = z_{i}^2 + c $$

is bounded, _i.e._ 

$$ \forall i \in \mathbb{N}, \left|z_{i}\right| \le b \in \mathbb{R}^+ $$

It can be demonstrated that, if for some $i$, $ \left|z_{i}\right| > 2 $, the iteration is 
guaranteed to be unbounded, and thus $c \notin \mathcal{M}$. This yields a practical criterion to compute an  
**approximate Mandelbrot set** $ \mathcal{M}_N$, containing as all complex numbers for which the first $N$ iterations
remain inside the circle with radius 2 (centered at the origin), _i.e._ for which $ \left|z_{i}\right| \le 2 $ for all 
$i\le{N}$.

The Mandelbrot set $\mathcal{M}$, or its approximation $\mathcal{M}_N$, is traditionally coloured black, while the 
other points, the points escaping outside the circle with radius 2 towards infinity, get a colour that indicates how 
fast they escape. Here is an example (from [wikipedia](https://en.wikipedia.org/wiki/Mandelbrot_set)):

![mandelbrot](public/644px-Mandel_zoom_00_mandelbrot_set.jpg)

## Assignment - the Mandelbrot competition

Take the complex numbers $c \in \mathbb{C}$ for which $\Re(c) \in \left[-2,1\right]$ and $\Im(c) \in \left[0,
4/3\right]$, _i.e._ about the upper half of the figure above (the lower half is symmetric). Compute the approximate 
mandelbrot sets $\mathcal{M}_{100}$, $\mathcal{M}_{1000}$ and $\mathcal{M}_{10000}$ and pixel densities $d$ of 50, 500, 
and 5000 pixels per unit length. You may use the center of the pixels for the points $c$. Time each of these 9 cases. 

| walltime[s] | _d_=50 | _d_=500 | _d_=5000 | sum     |
|-------------|--------|---------|----------|---------|
| _N_=100     |        |         |          |         |
| _N_=1000    |        |         |          |         |
| _N_=10000   |        |         |          |         |
| sum         |        |         |          | _Total_ |

***This a competition!*** 5/20 points are will be given to the winner, _i.e._ the one with the smallest total compute 
time _Total_ over the 9 cases, 4 to the second, and so on. The remaining 15 points are to be earned on the presentation.

As in every competition, there are a few ***rules***:

- Your code must be a ***Python program***, but you may use C++ or Fortran to build your own Python modules for speed.
- The timings must be run on ***a single compute node of [Vaughan](https://docs.vscentrum.
  be/en/latest/antwerp/tier2_hardware/vaughan_hardware.html?highlight=vaughan)***, 
  the Tier-2 VSC-cluster of the University of Antwerp. Every compute nodes has 64 cores, all of which you can use to 
  parallellise the work and increase the througput. 
- ***Every case must be computed in at most one job***. If you like, you may run all cases together in one job, but 
  splitting a case over more jobs is not allowed.
- Obviously, the github repo that you will use to store the different versions of your code, the presentation and 
  the results, must contain all necessary files to rerun your program, as to verify the correctness of the results and 
  the timings. 

Success! 