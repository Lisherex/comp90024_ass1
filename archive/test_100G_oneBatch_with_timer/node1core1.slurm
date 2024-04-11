#!/bin/bash

#SBATCH --time=00:25:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH -o ./cccAs1/src/test_100G_oneBatch_with_timer/result/node1core1.txt

module load GCCcore/11.3.0; module load Python/3.10.4

source ~/venvs/venv-3.10.4/bin/activate

module load mpi4py/3.0.2-timed-pingpong

time mpiexec python3 ./cccAs1/src/test_100G_oneBatch_with_timer/Main.py

deactivate
my-job-stats -a -n -s
