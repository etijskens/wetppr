#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=16 
#SBATCH --cpus-per-task=4
#SBATCH --time=00:05:00
#SBATCH --job-name hello-mpi4py
#SBATCH -o %x.%j.stdout
#SBATCH -e %x.%j.stderr

. ../env-lmod.sh foss

# Add the project directory to the PATH so the python script can find the hello_omp binary extension module
export PYTHONPATH=/data/antwerpen/201/vsc20170/wetppr/:${PYTHONPATH}
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OMP_PROC_BIND=true

# run the Python script hello-mpi4py.py on the requested resources
srun --quiet -n${SLURM_NTASKS} -c${SLURM_CPUS_PER_TASK} --exclusive --unbuffered python hello-mpi4py.py