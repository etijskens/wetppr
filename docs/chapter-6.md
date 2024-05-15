# Chapter 6 - Tools for parallellization

These tools can be used for parallelizing a problem on a HPC cluster (*e.g.* Vaughan), but also on your  local machine if you install MPI, mpi4py and dask_mpi. To execute a python script ``script.py`` in parallel  on Vaughan, you must execute a job script with the command

```shell
srun python script.py <script parameters>
```

This will automatically run the script with the requested resources. For more information about submitting  job scripts see [Submitting jobs on Vaughan][submitting-jobs-on-vaughan].

To run the python script in parallel on 4 CPUs on your local machine you must run this commmand in a terminal:

```shell
mpirun -np 4 python script.py
```

## Mpi4py

Mpi4py is a Python package that wraps the popular MPI framework for message passing between processes. It is very  flexible, but typically requires quite a bit of work to set up all the communication correctly.

Here are some useful links:

- [Mpi4py documentation](https://mpi4py.readthedocs.io/en/stable).
- The mpi4py documents the Python wrappers for MPI functions, not the wrapped functions themselves. The [MPI documentation](https://www.open-mpi.org/doc/) is therefor also useful.
- [A github repo with som simple mpi4py examples](https://github.com/jbornschein/mpi4py-examples).
- Some hints for setting up a master-slave configuration of cpus:
    - [MPI master slave](https://github.com/luca-s/mpi-master-slave)
    - [Get master to do work in a task farm](https://stackoverflow.com/questions/40508520/get-master-to-do-work-in-task-farm)

!!! note
    On your local machine you must first install a MPI library for your OS, before you can ``pip install mpi4py``.

## Dask-MPI

The Dask-MPI project makes it easy to deploy Dask from within an existing MPI environment, such as one created with  the common MPI command-line launchers mpirun or mpiexec. Such environments are commonly found in high performance  supercomputers, academic research institutions, and other clusters where MPI has already been installed. The dask  documentation is [here](https://docs.dask.org/en/stable/).

[Dask futures](https://docs.dask.org/en/stable/futures.html) provide a simple approach to distribute the computation  of a function for a list of arguments over a number of workers and gather the results. The approach reserves one cpu  for the scheduler (rank 0) and one for the client script (rank 1). All remaining ranks are ``dask`` workers. Here is  a typical example that computes the square of each item in an iterable using an arbitrary number of dask workers:

```python
from mpi4py import MPI
from dask_mpi import initialize
initialize()
# Create a Client object
from distributed import Client
client = Client()

def square(i):
    result = i*i
    # a print statement, just to see which worker is computing which result:
    print(f'rank {MPI.COMM_WORLD.Get_rank()}: {i=}**2 = {result}')
    # Note that the order of the output of the print statements does NOT 
    # necessarily correspond to the execution order.
    return result

if __name__ == "__main__":
    # Apply the square method to 0, 1, ..., 999 using the available workers
    futures = client.map(square, range(1000))
    # client.map() returns immediately after the work is distributed.
    # Typically, this is well before the actual work itself is finished.
    # Gather the results
    results = client.gather(futures)
    # client.gather() can only return after all the work is done, obviously.
    print('-*# finished #*-')
```

!!! note
    At the time of writing, dask is not installed as an LMOD module on the cluster. So you must install it yourself. Make sure you first source the ``wetppr-env.sh`` script mentioned in [LMOD modules][lmod-modules].

To install ``dask_mpi``, run:

```shell
> . path/to/wetppr-env.sh     # to set $PYTHONUSERBASE
> python -m pip install --user dask_mpi --upgrade
> python -m pip install --user dask distributed --upgrade
```

!!! note
    This installs ``dask_mpi``, ``dask`` and ``dask.distributed`` into the directory specified by ``$PYTHONUSERBASE``. This environment variable must also be available to the job. If ``$PYTHONUSERBASE`` is not set in your ``~/.bashrc`` file, you must set it in the job script.

!!! note
    `Dask-MPI` builds on `mpi4py`, so, MPI and mpi4py need to be available in your environment.
