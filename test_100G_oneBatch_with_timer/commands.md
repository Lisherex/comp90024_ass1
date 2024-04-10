`scp -r "E:\class\04_s1\Cluster and Cloud Computing\assignment1\master\test_100G_oneBatch_with_timer" yufeil10@spartan.hpc.unimelb.edu.au:/home/yufeil10/cccAs1/src`

`sbatch ./cccAs1/src/test_100G_oneBatch_with_timer/submit.sh`
`sprio -j 58230815`
`my-job-stats -j 58230815`

`vim ./cccAs1/src/test_100G_oneBatch_with_timer/node1core1.slurm`
`vim ./cccAs1/src/test_100G_oneBatch_with_timer/result/node1core1.txt `
`sprio -j 58230816`
`my-job-stats -j 58230816`

`vim ./cccAs1/src/test_100G_oneBatch_with_timer/node1core8.slurm`
`vim ./cccAs1/src/test_100G_oneBatch_with_timer/result/node1core8.txt`
`sprio -j 58230817`
`my-job-stats -j 58230817`

`vim ./cccAs1/src/test_100G_oneBatch_with_timer/node2core8.slurm`
`vim ./cccAs1/src/test_100G_oneBatch_with_timer/result/node2core8.txt`
`sprio -j 58230818`
`my-job-stats -j 58230818`


`scp -r yufeil10@spartan.hpc.unimelb.edu.au:/home/yufeil10/cccAs1/src/test_100G_oneBatch_with_timer/result "E:\class\04_s1\Cluster and Cloud Computing\assignment1\master\test_100G_oneBatch_with_timer"`

