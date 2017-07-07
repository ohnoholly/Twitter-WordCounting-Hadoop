#Twitter's WordCounting On Hadoop
***
Author: Han Wang <br>
This project is to record how I utlize cloud computing resources in the SNIC Science Cloud(SSC), which is a Swedish national resource (a community cloud) that provides Infrastructure-as-a-Service (IaaS), to build up a virtual machines for Hadoop Files System. SSC is built using  OpenStack cloud software  and Ceph storage. I implement MapReduce with counting Swedish pronouns  “han”, “hon”, “den”, “det”, “denna”, “denne”, and the gender neutral pronoun “hen”.
***
###System Benchmark

| Operation System | Flavor Name | RAM Size |  VCPUs | Disk Storage | Availability Zone| Network|
|:--------:|:-----------:|:--------:|:------:|:------------:|:------------:|:-------------:|
|  Linux 4.4.0-75-generic x86_64  |  ssc.xlarge  |    16 GB   | 8 VCPU |     160 GB     | nova |  Internal IPv4 Network |

###Steps for starting VM in SSC
<ol>
<li> Create a new SSH keypair.
<li> Start an instance by booting an image.
<li>Assign a floating IPs to the instance.
</ol>

###Starting HDFS service 
For starting the Hadoop, we need to access the instance and get into the VM. The login Command line is as following:<br>

```
$ sudo ssh -i keypair.pem ubuntu@FloatingIPAddress
```
Next, switch to super-user “root".<br>

```
$ sudo bash
```
Next, switch to Hadoop user “hduser"<br>

```
$ su - hduser
```
Next, because Hadoop is already existed and installed in this VM, we just need to format and start it. <br>

```
$ cd /home/hduser
$ ./format_hdfs.sh
```
Next, Start the HDFS services. <br>

```
$ ./start_hadoop.sh
```
Next, Check if all the services are working. “jps” is the command to see the Java Processes. <br>

```
$ jps
```
The outout should look like this:

```
1089 NodeManager
2837 Jps
360 NameNode
936 ResourceManager
540 DataNode
749 SecondaryNameNode
```
Finally, after using HDFS, remember to stop the services.<br>

```
$ ./stop_hadoop.sh
```
In addition, if the DataNode is not working, we need to restart the HDFS services by following steps:<br>

```
$ ./stop_hadoop.sh
$ sudo rm -r /app/hadoop/tmp/*
$ ./format_hdfs.sh
$ ./start_hadoop.sh
```

###Move File to HDFS
In this project, we want to analyze a dataset of ~5.000.000 Twitter tweets collected using Twitters datastream API. The dada is in JSON format. The information of each useful field is in the document. <br>
[Tweets field](https://dev.twitter.com/overview/api/tweets)<br>
All the needed data is available in the /home/hduser folder. 
We need to extract the data from the zip file. The Command line for extracting. 

```
$ tar -zxvf zipfilename.tar.gz
```
The data is ready in the local disk. But we still need to move these files to the HDFS. I follow the tutorial:<br>
http://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/ <br>

```
$ cd /usr/local/hadoop
$ bin/hadoop dfs -copyFromLocal (localdiskpath) (targetpath)
$ bin/hadoop dfs -ls (targetpath)
```

The third command line above is to check if the data is moved to HDDFS sucessfully. <br>

###Prepare  Mapper.py and Reducer.py
Two python files are avaiable in this project. One is mapper.py and reducer.py. The mapper.py contains the method of praseing JSON file.<br> 

###Run the MapReduce Job
Now that everything is prepared, we can finally run our Python MapReduce job on the Hadoop cluster.<br>
Note: The command line is needed to be modified if the location of jar file is different. 

```
$ bin/hadoop jar contrib/streaming/hadoop-*streaming*.jar -mapper /home/hduser/mapper.py -reducer /home/hduser/reducer.py -input /filepath -output /output
```
If the program works successfully, there should be these messages:<br>

```
17/07/06 15:19:54 INFO mapred.LocalJobRunner: reduce task executor complete.
17/07/06 15:19:54 INFO mapreduce.Job:  map 100% reduce 100%
17/07/06 15:19:54 INFO mapreduce.Job: Job job_local636479579_0001 completed successfully

```
Finnally, to check the result, we use this command:

```
$ bin/hadoop dfs -cat /output/part-00000
```