**Upload files from LOCAL to SPARTAN**<br />
`scp -r "E:\class\04_s1\Cluster and Cloud Computing\assignment1\master\test_100G_oneBatch" yufeil10@spartan.hpc.unimelb.edu.au:/home/yufeil10/cccAs1/src`

**Submit all 3 jobs through one .sh file**<br />
`sbatch ./cccAs1/src/test_100G_oneBatch/submit.sh`<br />
`sprio -j 58229354`<br />
`my-job-stats -j 58229354`<br />

**Check Job Status for node1core1**<br />
`vim ./cccAs1/src/test_100G_oneBatch/node1core1.slurm`<br />
`vim ./cccAs1/src/test_100G_oneBatch/result/node1core1.txt `<br />
`sprio -j 58229355`<br />
`my-job-stats -j 58229355`<br />

**Check Job Status for node1core8**<br />
`vim ./cccAs1/src/test_100G_oneBatch/node1core8.slurm`<br />
`vim ./cccAs1/src/test_100G_oneBatch/result/node1core8.txt`<br />
`sprio -j 58229356`<br />
`my-job-stats -j 58229356`<br />

**Check Job Status for node2core8**<br />
`vim ./cccAs1/src/test_100G_oneBatch/node2core8.slurm`<br />
`vim ./cccAs1/src/test_100G_oneBatch/result/node2core8.txt`<br />
`sprio -j 58229357`<br />
`my-job-stats -j 58229357`<br />

**Download Results from SPARTAN to LOCAL**<br />
`scp -r yufeil10@spartan.hpc.unimelb.edu.au:/home/yufeil10/cccAs1/src/test_100G_oneBatch/result "E:\class\04_s1\Cluster and Cloud Computing\assignment1\master\test_100G_oneBatch\result"`<br />

