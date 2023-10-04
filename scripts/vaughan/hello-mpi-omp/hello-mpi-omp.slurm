#!/bin/bash
#SBATCH --ntasks=64 --cpus-per-task=1
#SBATCH --time=00:05:00
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --job-name mpi4py_hello_world
#SBATCH -o %x.%j.stdout
#SBATCH -e %x.%j.stderr

module --force purge
module load calcua/2020a
module load Python
module list

srun  python mpi4py_hello_world.py
