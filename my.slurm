#!/bin/bash
#SBATCH --time=00:15:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH -o output.txt

module load python/3.7.4
mkdir ~/virtualenv
virtualenv ~/virtualenv/python3.7.4
source ~/virtualenv/python3.7.4/bin/activate

module load mpi4py/3.0.2-timed-pingpong
pip install numpy

time mpiexec python3 main.py
deactivate

my-job-stats -a -n -s