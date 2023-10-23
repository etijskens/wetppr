import itertools
import os
jobid  = os.getenv('SLURM_JOB_ID')
stepid = os.getenv('SLURM_STEP_ID')
pid    = os.getpid()
affinity = os.sched_getaffinity(0) # set of the CPUs used by the current MPI proces

from mpi4py import MPI
comm = MPI.COMM_WORLD


def print_environment_variable(name):
    value = os.getenv(name)
    print(f"${{{name}}}={value}")


if __name__ == '__main__':
    # print some environment variables
    if comm.rank == 0:
        print_environment_variable('SLURM_NTASKS')
        print_environment_variable('SLURM_CPUS_PER_TASK')

    print(f'jobid.stepid={jobid}.{stepid}, MPI_rank={comm.rank}/{comm.size}, {pid=} : affinity={affinity}')

    
    