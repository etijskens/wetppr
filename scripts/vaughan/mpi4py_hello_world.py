from mpi4py import MPI

comm = MPI.COMM_WORLD

if __name__ == '__main__':
    print(f'Hello from rank={comm.rank}/{comm.size}')
