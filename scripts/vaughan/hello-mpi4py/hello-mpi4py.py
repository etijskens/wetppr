import sys
print(f"{sys.path=}")

from mpi4py import MPI
from wetppr.hello_omp import hello_omp_from 

comm = MPI.COMM_WORLD

if __name__ == '__main__':
    print(f'Hello from MPI_rank={comm.rank}/{comm.size}')
    hello_omp_from(comm.rank)
