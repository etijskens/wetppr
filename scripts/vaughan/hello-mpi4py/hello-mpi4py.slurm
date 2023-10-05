#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=16 --cpus-per-task=4
#SBATCH --time=00:05:00
#SBATCH --job-name hello-mpi4py
#SBATCH -o %x.%j.stdout
#SBATCH -e %x.%j.stderr

module --force purge
module load calcua/2022a
module load SciPy-bundle
module list

# Add the project directory to the PATH so the python script can find the hello_omp binary extension module
export PATH=/data/antwerpen/201/vsc20170/wetppr/:${PATH}
echo "PATH = ${PATH}"

# run the Python script hello-mpi4py.py on the requested resources
srun -n${SLURM_NTASKS} -c${SLURM_CPUS_PER_TASK} python hello-mpi4py.py