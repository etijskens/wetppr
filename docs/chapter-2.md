# Chapter 2 - Aspects of modern CPU architecture

[//]: # (script below is for allowing for MathJax rendering of LateX expressions)

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

You do not have to be a CPU architecture specialist in order to be able to write efficient code. However, there are 
a few aspects of CPU architecture that you should understand.

## The hierarchical structure of CPU Memory

CPU memory of modern CPUs is hierarchically organised:

- Each processing unit (or core) has a number of **registers** (~1 kB) and vector registers on which instructions can 
  immediately operate (latency = 0 cycles). The registers are connected to  
- a dedicated **L1 cache** (~32 kB per core), with a latency of ~ 1 cycle. This is in turn 
  connected to:  
- a dedicated **L2 cache**, (~256 kB per core), with a latency of ~10 cycles. This is in turn connected to: 
- a shared **L3 cache**, (~2 MB per core), with a latency of ~50 cycles. This is  connected to:
- the **main memory** (256 GB - 2 TB), with a latency of ~200 cycles.

The cores and the caches are on the same chip. For this reason they are considerably faster than the main memory. 
Faster memory is more expensive and therefor smaller. When an instruction needs a data item in a register, the CPU 
looks first in the L1 cache, if it is there it will it to the register that was requested. Otherwise, the CPU looks 
in L2. If it is there, it is copied to L1 and the register. Otherwise, the CPU looks in L3. If it is there, it is 
copied to L2, L1 and the register. Otherwise, the CPU looks copies the **cache line** surrounding the data item to 
L3, L2, L1 and the data item itself to the register. A cache line is typically 64 bytes long and thus can contain 4 
double precision floating point numbers or 8 single precision numbers. The main consequence of this strategy is that 
if the data item is part of an array, the next elements of that array will also be copied to L1 so that when 
processing the array the latency associated with main memory is amortized over 4 or 8 iterations. In addition, the 
CPU will notice when it is processing an array and prefetch the next cache line of the array in order to avoid that 
the processor has to wait for the data again. This strategy for loading data leads to two important best practices for 
making optimal use of the cache.

1. **Spatial locality**: Organize your data layout in main memory in a way that data in a cache line are mostly 
   needed together. 
2. **Temporal locality**: Organize your computations in a way that once a cache line is in L1 cache, as much as 
   possible computations on that data are carried out. This favors a high computational intensity (see below). 
   Common techniques for this are **loop fusion** and **tiling**. 

### Loop fusion

Here are two loops over an array `x`

```python
for xi in x:
    do_something_with(xi)
for xi in x:
    do_something_else_with(xi)
```
If the array `x` is big, too big to fit in the cache, the above code would start loading `x` elements into the cache,
cach line by cache line. Since `x` is to large to fit in the cache, at some point, when the cache is full, the CPU 
will start to evict the cache lines that were loaded long time a go ane are no more used to replace them with new 
cache lines. By the time the first loop finishes, the entire beginning of the `x` array has been evicted and the 
scond loop can start to transfer `x` again from the main memory to the registers, cache line by cache lina. this 
violiate the temporal locality principle. So, it incurs twice the data traffic. Loop fusion fuses the two loops into 
one and does all computations needed on `xi` when it is in the cache. 

```python
for xi in x:
    do_something_with(xi)
    do_something_else_with(xi)
```
The disadvantage of loop fusion is that the body of the loop may become too large and require more vector registers 
than are available. At that point some computations may be done sequentially and performance may suffer. 

### Tiling

Tiling is does the opposite. Ik keeps the loops separate but restricts them to chunks of `x` which fit in L1 cache.
```python
for chunk in x: # chunk is a slice of x that fits in L1
    for xi in chunk:
        do_something_with(xi)
    for xi in chunk:
        do_something_else_with(xi)
```
Again all computations that need to be done to `xi` are done when it is in L1 cache. Again the entire `x` array is 
transferred only once to the cache. A disadvantage of tiling is that the chunksize need to be tuned to the size of L1, 
which may differ on different machines. Thus, this approach is not **cache-oblivious**. Loop fusion, on the other hand,
is cache-oblivious. 

...

The above strategy for loading data has also important consequences for the layout of data arrays and for  
loops over arrays in terms of performance (see below). 

The hierarchical structure of processor memory requires good understanding to write efficient programs and it may 
seem an overly complex solution for a simple problem, but it isn't. It is a good compromise to the many faces of a 
truly complex problem. There is an excellent presentation on this matter by Scott Meyers: [*CPU Caches and Why 
You Care*](https://www.youtube.com/watch?v=WDIkqP4JbkE), an absolute must see for this course.

## Intra-core parallellisation features 

Modern CPUs are designed to (among other things) process loops as efficiently as possible, as loops typically 
account for a large part of the work load of a program. To make that possible CPUs use two important concepts: 
**instruction pipelining** (ILP) and **SIMD vectorisation**. 

### Instruction pipelining

Instruction pipelining is very well explained [here](https://en.wikipedia.org/wiki/Instruction_pipelining).

Basically, instructions are composed of micro-instructions (typically 5), each of which are executed in separate 
hardware units of the CPU. By executing the instructions sequentially, only one of those units would be active at a 
time: namely, the unit responsible for the current micro-instruction. By adding extra instruction registers, all 
micro-instruction hardware units can work simultaneously, but on micro-instructions pertaining to different but 
consecutive instructions. In this way, on average 5 (typically) instructions are being executed in parallel. This is 
very useful for loops. There are a couple of problems that may lead to **pipeline stalls**, situations where the 
pipeline comes to halt. 

1. A data element is requested that is not in the L1 cache. It must be fetched from deeper cache levels or even 
   from main memory. This is called a **cache miss*. A L1 cache miss means that the data is not found in L1, but is 
   found in L2. In a L2 cache miss it is not found in L2 but it is in L3, and a L3 cache miss, or a cache miss *tout 
   court* de data is not found in L3 and has to be fetched from main memory. The pipeline stops executing for a 
   number of cycles corresponding to the latency of that cache miss. Data cache misses are the most important cause 
   of pipeline stalls and as the latency can be really high (~100 cycles).  
2. A instruction is needed that is not in the L1 instruction cache. This may sometimes happen when a (large) 
   function is called that is not inlined. Just as for a data cache miss, the pipeline stalls for a number of cycles 
   corresponding to the latency of the cache miss, just as for a data cache miss. 
3. You might wonder how a pipeline proceeds when confronted with a branching instruction, a condition that has to be 
   tested, and must start executing different streams of instructions depending on the outcome (typically 
   if-then-else constructs). Here's the thing: it guesses the outcome of the test and starts executing the 
   corresponding branch. As soon as it notices that it guessed wrong, which is necessarily after the condition has been 
   tested, it stops, steps back and restarts at the correct branch. Obviously, the performance depends on how well 
   it guesses. The guesses are generally rather smart. It is able to recognize temporal patterns, and if it doesn't 
   find one, falls back on statistics. Random outcomes of the condition are thus detrimental to performance as its
   guess will be wrong at least half the time.

### Recommendations for loops processing arrays

1. **The longer the loop, the better**. Typically, at the begin and end of the loop thee pipeline is not full. 
   When the loop is long, these sections can be amortized with respect to the inner section, where the pipeline is 
   full. 
2. Loops with branches should be **predictable**. The outcome of unpredictable branches will be guessed wrongly, 
   causing pipeline stalls. Sometimes it may be worthwile to sort the array according to the probability of the 
   outcome if this work can be amortized over many loops.
2. To profit as much as possible from the operation of the caches, loops should access data **contiguously** and 
   with **unit stride**. This assures that
    - at the next iteration of the loop the data element needed is already in the L1 Cache and can be accessed 
      without delay,
    - vector registers can be filled efficiently because they need contiguous elements from the input array.
3. Loops should have **high computatonal intensity**. The computational intensity $I_c$ is defined as $ I_c = \frac
   {n_{cc}}{n_{rw}} $, with $n_{cc}$ the number of compute cycles and $n_{rw}$ the total number of bytes read and 
   written. A high computational intensity means many compute cycles and little data traffic to/from memory and thus 
   implies that there will be no pipeline due to waiting for data to arrive. This is a compute bound loop. Low 
   computational intensity, on the other hand, will cause many pipeline stalls by waiting for data. This is a 
   memory bound loop. Here, it is the bandwidth (the speed at which data can be transported from main memory 
   to the registers) that is the culprit, rather than the latency. 
   
### Recommendations for data structures

The unit stride for loops recommendation translates into a recommendation for data structures. Let's take Molecular 
Dynamics as an example. Object Oriented Programming (OOP) would propose a Atom class with properties for mass $m$, 
position $\textbf{r}$, velocity $\textbf{v}$, acceleration $\textbf{a}$, and possibly others as well, but let's 
ignore those for the time being. Next, the object oriented programmer would create an array of Atoms. This approach 
is called an **array of structures** (AoS). The AoS approach 
leads to a data layout in memory like | $m_0$, $r_{x0}$, $r_{y0}$, $r_{z0}$, $v_{x0}$, $v_{y0}$, $v_{z0}$, $a_{x0}$, |
$a_{y0}$, $a_{z0}$, $m_1$, $r_{x1}$, $r_{y1}$, $r_{z1}$, $v_{x1}$, $v_{y1}$, | $v_{z1}$, $a_{x1}$, $a_{y1}$, $a_{z1}
$, $m_2$, $r_{x2}$, $r_{y2}$, $r_{z2}$, | $v_{x2}$, $v_{y2}$, $v_{z2}$, $a_{x2}$, $a_{y2}$, $a_{z2}$, ... Assume we 
store the properties as single precision floating point numbers, hence a cache line spans 8 values. We marked the cache 
line boundaries in the list above with vertical bars. Suppose for some reason we need to find all atoms $j$ for 
which $r_{xj}$ is between $x_{lwr}$ and $x_{upr}$. A loop over all atoms $j$ would test $r_{xj}$ and remember the 
$j$ for which the test holds. Note that every cache line contains at most one single data item that we need in this 
algorithm. some cache lines will even contain no data items that we need. For every data iten we need, a new cache 
line must be loaded. This is terribly inefficient. There is a lot of data traffic, only 1/8 of which is useful and the 
bandwidth will saturate quickly. Vectorisation would be completely useless. To fill the vector register we would 
need 8 cache lines, most of which would correspond to cache misses and cost hundreds of cycles, before we can do 8 
comparisons at once. The AoS, while intuitively very attractive, is clearly a disaster as it comes to performance. 
The - much better - alternative data structure is the SoA, **structure of Arrays**. This creates an AtomContainer 
class (to stay in the terminology of Object Oriented progrmming) containing an array of length $n_{atoms}$ for each 
property. In this case there would be arrays for $m$, $r_x$, $r_y$, $r_z$, $v_x$, $v_y$, $v_z$, $a_x$, $a_y$, $a_z$. 
Now all $r_x$ are stored contiguously in memory and every item in a cache would be used. Only one cache line would 
be needed to fill a vector register. Prefetching would do a perfect job. The SoA data structure is much more 
efficient, and once you get used to it, almost equally intuitive from an OOP viewpoint. Sometimes there is 
discussion about storing the coordinates of a vector, e.g. $\textbf{r}$ as per-coordinate arrays, as above, or as an 
array of vectors. The latter makes is more practical to define vector functions like magnitude, distance, dot and 
vector products, ... but they make it harder to SIMD vectorise those functions efficiently, because contiguous data 
items need to be moved into different vector registers.  

!!! Tip 
    There is no silver bullet. All approaches have advantages and disadvantages, some may appear in this situation 
    and others in another situation. The only valid reasoning is: **numbers tell the tale** (*meten is weten*): 
   measure the performance of your code. Measure it twice, than measure again. 