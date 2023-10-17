from mpi4py import MPI
comm = MPI.COMM_WORLD

import sys
import os
if comm.rank == 0:
    print(f"{os.environ['SLURM_NTASKS']=}")
    print(f"{os.environ['SLURM_CPUS_PER_TASK']=}")
    print(f"{os.environ['OMP_NUM_THREADS']=}")
    print(f"{os.environ['NUMBA_NUM_THREADS']=}")
    print(f"{os.environ['NUMBA_THREADING_LAYER']=}")

import numba
if comm.rank == 0:
    print(f"{numba.config.THREADING_LAYER=}")
    print(f"{numba.config.NUMBA_NUM_THREADS=}")

from wetppr.hello_omp import info, hello_omp_from
import numpy as np

@numba.njit(parallel=True)
def hello_numba_from(mpi_rank):
    for i in numba.prange(numba.config.NUMBA_NUM_THREADS):
        print(f"hello_numba_from)MPI_rank={mpi_rank})  omp_thread={numba.get_thread_id()}/{numba.get_num_threads()}")


if __name__ == '__main__':
    print(f'Hello from MPI_rank={comm.rank}/{comm.size}  aff={os.sched_getaffinity(0)}')
    info(comm.rank)
    hello_numba_from(comm.rank)
    hello_omp_from(comm.rank)
    
    