import os
jobid  = os.getenv('SLURM_JOB_ID')
stepid = os.getenv('SLURM_STEP_ID')
pid    = os.getpid()
affinity = os.sched_getaffinity(0) # set of the CPUs used by the current MPI proces

from mpi4py import MPI
comm = MPI.COMM_WORLD


def print_environment_variable(name):
    """Print the name and the value of an environment value."""
    value = os.getenv(name)
    print(f"${{{name}}}={value}")


if __name__ == '__main__':
    # Print some environment variables (only if the MPI rank is 0)
    if comm.rank == 0:
        print_environment_variable('SLURM_NTASKS')
        print_environment_variable('SLURM_CPUS_PER_TASK')

    # Print a line with the job-id, job-step-id, MPI rank, total number of MPI
    # processes, process id, and the affinity (the id of the CPU on which 
    # the MPI process is running). Every MPI process will print one line.
    print(f'jobid.stepid={jobid}.{stepid}, MPI_rank={comm.rank}/{comm.size}, {pid=} : affinity={affinity}')
          