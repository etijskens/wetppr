#!/bin/bash
### The line above is the shebang. It specifies the interpreter for the script. Always /bin/bash.

### Submit this job from the parent directory as:
### > cd path/to/wetppr/scripts/vaughan/hello-mpi4py
### > sbatch hello-mpi4py.slurm

### Slurm job script parameters ################################################
### Accounting info. Specify the account from which credits will be taken to 
### execute this job. At the time of writing (11/2023) only applicable on 
### the VSC Tier-1 computer Hortense and the Tier-2 supercomputers at KU Leuven,
### soon also in Tier-2 supercomputers at UAntwerpen. 
### SBATCH --account=<account-name>

### Specify the job name
#SBATCH --job-name hello-mpi4py

### Redirect output written to stdout to file <job-name>.<job-id>.stdout 
### Redirect output written to stderr to file <job-name>.<job-id>.stderr
### This groups your files nicely in a alphabetical listing.
#SBATCH -o %x.%j.stdout
#SBATCH -e %x.%j.stderr

### Slurm resource specifications 
### Request 1 compute node
#SBATCH --nodes=1

### Request 16 MPI processes
#SBATCH --ntasks=16 

### Request 1 CPU per MPI process (no hybrid OpenMP-MPI)
#SBATCH --cpus-per-task=1

### Tell Slurm that you expect the job to end in 5 minutes.
### (Abort the job if it takes longer).
#SBATCH --time=00:05:00

### Prepare the environment for the job ########################################
### Source the env-lmod.sh script to loads the LMOD modules needed.
### We requeste it to use the foss toolchain. 
source ../env-lmod.sh foss

### Specify the computational work #############################################
### Run the Python script hello-mpi4py.py on the requested resources by calling 
### srun (this is a Slurm command)
srun -n${SLURM_NTASKS} -c${SLURM_CPUS_PER_TASK} --exclusive --unbuffered python hello-mpi4py.py