# BDP1 project

## COMPUTATIONAL CHALLENGE
The computational challenge consists on building an infrastructure to align 300 million of sequences against the human reference genome using the Burrows-Wheeler Aligner (BWA). The infrastructure contains three different sites built on different Google Cloud projects to simulate the geographical distribution. The first site will be the High Throughput Computing (HTC) site, with more copies of the same program run in parallel. 
## HIGH THROUGHPUT COMPUTING (HTC) SITE
HTC site is designed to run copies of the same program in parallel. It consists of one master node (htc-instance) and two working nodes (slave-2 has been created later as an image of slave-1). All instances run the CentOS 7 operating system with e2-standard-2 type machine (2 vCPUs and 8 GB of memory).

![image](https://github.com/jesusch10/bdp1-project/assets/136498796/d855d570-032a-43db-ac41-2c2690403886)

Commands below show how to create a SSH key along with its “.pub” file that then is manually added to the instance metadata, and how to access the VM instances:
```
ssh-keygen -t rsa -f ./key_project
ssh -i key_project jesus@<instance_external_ip>
```
After creating the storage site (point XXX), the new volume is attached to the htc-instance:
```
sudo su                       # Become superuser
fdisk /dev/sdb                # Access the partition menu and type commands: p, n, p (keep defaults), w
mkfs.ext4 /dev/sdb1           # Create the ext4 filesystem
mkdir /data2                  # Create a mountpoint for the new filesystem
vi /etc/fstab                 # Edit the fstab file to add this line: /dev/sdb1     /data2  ext4 defaults 0 0
mount -a                      # Mount all the filesystem listed in the fstab file
chmod 777 /data2/             # Change the permissions so the master and the nodes can read, write, and execute in the volume
```
Install the NFS server in the htc-instance:
```
yum install nfs-utils rpcbind
systemctl enable nfs-server
systemctl enable rpcbind
systemctl enable nfs-lock
systemctl enable nfs-idmap
systemctl start rpcbind
systemctl start nfs-server
systemctl start nfs-lock
systemctl start nfs-idmap
systemctl status nfs
vim /etc/exports             # Add this line: /data2  <private IP of the slave-1 instance (client)>(rw,sync,no_wdelay)
exportfs -r
```
Install the NFS client in the slave-1 instance:
```
sudo su
yum install nfs-utils
mkdir /data2
mount -t nfs -o ro,nosuid <private IP of the htc-instance (server)>:/data2 /data2
umount /data2
vim /etc/fstab             # Add this line: <private IP of the htc-instance (server)>:/data2 /data2   nfs defaults        0 0
mount -a
```
Display the final disk filesystem in each instance with `df -h`:

![image](https://github.com/jesusch10/bdp1-project/assets/136498796/c2071a72-13ed-441a-9075-2c83a1bacad1)

Installing HTCondor dependencies and packages both in htc-instance and slave-1 instance:
```
yum install wget
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum localinstall epel-release-latest-7.noarch.rpm
yum clean all
wget http://research.cs.wisc.edu/htcondor/yum/repo.d/htcondor-stable-rhel7.repo
cp htcondor-stable-rhel7.repo /etc/yum.repos.d/
yum install condor-all
```
In the htc-instance, next lines are added when running `vim /etc/condor/condor_config`:
```
CONDOR_HOST = <htc-insta private IP (master)>
DAEMON_LIST = COLLECTOR, MASTER, NEGOTIATOR, STARTD, SCHEDD
HOSTALLOW_READ = *
HOSTALLOW_WRITE = *
HOSTALLOW_ADMINISTRATOR = *
```
In the slave-1 instance, next lines are added when running `vim /etc/condor/condor_config`:
```
CONDOR_HOST = <htc-insta private IP (master)>
DAEMON_LIST = MASTER, STARTD
HOSTALLOW_READ = *
HOSTALLOW_WRITE = *
HOSTALLOW_ADMINISTRATOR = *
```
Enabling and starting HTCondor both in the htc-instance and slave-1 instance:
```
systemctl start condor
systemctl enable condor
```
Display the HTCondor status with `systemctl status condor`:

![image](https://github.com/jesusch10/bdp1-project/assets/136498796/48e3afdf-a4b0-4b6e-9bfb-6eed38eafa17)







