`scp -r "E:\class\04_s1\Cluster and Cloud Computing\assignment1\master\test_100G_oneBatch" yufeil10@spartan.hpc.unimelb.edu.au:/home/yufeil10/cccAs1/src`

`sbatch ./cccAs1/src/test_100G_oneBatch/submit.sh`
`sprio -j 58229354`
`my-job-stats -j 58229354`

`vim ./cccAs1/src/test_100G_oneBatch/node1core1.slurm`
`vim ./cccAs1/src/test_100G_oneBatch/result/node1core1.txt `
`sprio -j 58229355`
`my-job-stats -j 58229355`

`vim ./cccAs1/src/test_100G_oneBatch/node1core8.slurm`
`vim ./cccAs1/src/test_100G_oneBatch/result/node1core8.txt`
`sprio -j 58229356`
`my-job-stats -j 58229356`

`vim ./cccAs1/src/test_100G_oneBatch/node2core8.slurm`
`vim ./cccAs1/src/test_100G_oneBatch/result/node2core8.txt`
`sprio -j 58229357`
`my-job-stats -j 58229357`


`scp -r yufeil10@spartan.hpc.unimelb.edu.au:/home/yufeil10/cccAs1/src/test_100G_oneBatch/result "E:\class\04_s1\Cluster and Cloud Computing\assignment1\master\test_100G_oneBatch\result"`

