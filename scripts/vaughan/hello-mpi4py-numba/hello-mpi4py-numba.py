import itertools
import os
jobid  = os.getenv('SLURM_JOB_ID')
stepid = os.getenv('SLURM_STEP_ID')
pid    = os.getpid()
affinity = os.sched_getaffinity(0) # set of the CPUs used by the current MPI proces

from mpi4py import MPI
comm = MPI.COMM_WORLD

import numba # must come after os.sched_getaffinity(0) (if not, os.sched_getaffinity(0)
# will only report the CPU on which the current MPI process runs!)

def ranges(i):
    """Turn a sorted set of integers into a string of comma-separate ranges."""
    r = list()
    for a, b in itertools.groupby(enumerate(i), lambda pair: pair[1] - pair[0]):
        b = list(b)
        if len(b) == 1:
            r.append('%i' % (b[0][1]))
        else:
            r.append('%i-%i' % (b[0][1], b[-1][1]))
    return ','.join(r)


def print_environment_variable(name):
    value = os.getenv(name)
    print(f"${{{name}}}={value}")


@numba.njit(parallel=True)
def omp_parallel_section(mpi_rank):
    """Start an OpenMP parallel section in which each thread prints a message."""
    for i in numba.prange(numba.config.NUMBA_NUM_THREADS):
        print(f"hello_numba_from(MPI_rank={mpi_rank})  omp_thread={numba.get_thread_id()}/{numba.get_num_threads()}")
        
        
if __name__ == '__main__':
    # print some environment variables
    if comm.rank == 0:
        print_environment_variable('SLURM_NTASKS')
        print_environment_variable('SLURM_CPUS_PER_TASK')
        print(f"{numba.config.THREADING_LAYER=}")
        print_environment_variable('NUMBA_THREADING_LAYER')
        print_environment_variable('OMP_NUM_THREADS')
        print_environment_variable('NUMBA_NUM_THREADS')
        print(f"{numba.config.NUMBA_NUM_THREADS=}")

    print(f'jobid.stepid={jobid}.{stepid}, MPI_rank={comm.rank}/{comm.size}, {pid=} : affinity={ranges(sorted(affinity))}')

    omp_parallel_section(comm.rank)
    
    