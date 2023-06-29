# BDP! project

## COMPUTATIONAL CHALLENGE
The computational challenge consists on building an infrastructure to align 300 million of sequences against the human reference genome using the Burrows-Wheeler Aligner (BWA). The infrastructure contains three different sites built on different Google Cloud projects to simulate the geographical distribution. The first site will be the High Throughput Computing (HTC) site, with more copies of the same program run in parallel. 
## HIGH THROUGHPUT COMPUTING (HTC) SITE
HTC site is designed to run copies of the same program in parallel. It consists of one master node (htc-instance) and two working nodes (slave-2 has been created later as an image of slave-1). All instances run the CentOS 7 operating system with e2-standard-2 type machine (2 vCPUs and 8 GB of memory).

Commands below show how to create a SSH key along with its “.pub” file that then is manually added to the instance metadata, and how to access the VM instances:
