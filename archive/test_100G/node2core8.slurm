#!/bin/bash

#SBATCH --time=00:25:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH -o node2core8.txt

module load GCCcore/11.3.0; module load Python/3.10.4

source ~/venvs/venv-3.10.4/bin/activate

module load mpi4py/3.0.2-timed-pingpong

time mpiexec python3 ./cccAs1/src/test_100G/test_100G.py

deactivate
my-job-stats -a -n -s
