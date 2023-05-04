from mpi4py import MPI

if __name__ == '__main__':
    print(f'rank={MPI.COMM_WORLD.Get_rank()}/{MPI.COMM_WORLD.Get_size()}')
