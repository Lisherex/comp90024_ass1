#!/bin/bash

# Submit node1core1.slurm
node1core1_id=$(sbatch --parsable ./cccAs1/src/test_100G_oneBatch_with_timer/node1core1.slurm)
echo "Submitted node1core1.slurm; ID: $node1core1_id"

# Submit node1core8.slurm
node1core8_id=$(sbatch --parsable ./cccAs1/src/test_100G_oneBatch_with_timer/node1core8.slurm)
echo "Submitted node1core8.slurm; ID: $node1core8_id"

# Submit node2core8.slurm
node2core8_id=$(sbatch --parsable ./cccAs1/src/test_100G_oneBatch_with_timer/node2core8.slurm)
echo "Submitted node2core8.slurm; ID: $node2core8_id"