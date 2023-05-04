#!/bin/bash
#SBATCH --ntasks=64 --cpus-per-task=1
#SBATCH --time=00:05:00
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=engelbert.tijskens@uantwerpen.be
#SBATCH --job-name hello_world
#SBATCH -o %x.%j.stdout
#SBATCH -e %x.%j.stderr

module --force purge
module load calcua/2021a
module load Python

srun --mpi=pmix python hello_world.py
