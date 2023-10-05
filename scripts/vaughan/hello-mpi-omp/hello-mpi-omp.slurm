#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks=64 --cpus-per-task=2
#SBATCH --time=00:05:00
#SBATCH --job-name hello-mpi-omp
#SBATCH -o %x.%j.stdout
#SBATCH -e %x.%j.stderr

module --force purge
module load calcua/2022a
module load intel
module list

# build the program _build/hello-mpi-omp
module load CMake
mkdir -p _build
cd _build
cmake ..
cmake --build .
cd ..

# set some environment variables to distribute the cpus optimally over the MPI processes
export OMP_PROC_BIND=true
export I_MPI_PIN_DOMAIN=omp,compact
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

# run the program _build/hello-mpi-omp on the requested resources
srun --quiet -n${SLURM_NTASKS} -c${SLURM_CPUS_PER_TASK} --exclusive --unbuffered _build/hello-mpi-omp