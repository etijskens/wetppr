from mpi4py import MPI
from dask_mpi import initialize

initialize()
# Create a Client object
from distributed import Client

client = Client()


def square(i):
    result = i * i
    # A print statement, just to see which worker is computing which result:
    print(f'rank {MPI.COMM_WORLD.Get_rank()}: {i=}**2 = {result}')
    # Note that t he order of the output of the print statements is NOT chronological.
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
