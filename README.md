# BDP1 project

## 1. Computational challenge:
The computational challenge consists on building an infrastructure to align 300 million of sequences against the human reference genome using the Burrows-Wheeler Aligner (BWA). The infrastructure contains three different sites built on different Google Cloud projects to simulate the geographical distribution. The first site will be the High Throughput Computing (HTC) site, with more copies of the same program run in parallel. 
## 2. High throughput computing (HTC) site:
### 2.1 Setting up the environment:
HTC site is designed to run copies of the same program in parallel. It consists of one master node (htc-instance) and two working nodes (slave-2 has been created later as an image of slave-1). All instances run the CentOS 7 operating system with e2-standard-2 type machine (2 vCPUs and 8 GB of memory).

![image](https://github.com/jesusch10/bdp1-project/assets/136498796/d855d570-032a-43db-ac41-2c2690403886)

Commands below show how to create a SSH key along with its `.pub` file that then is manually added to the instance metadata, and how to access the VM instances:
```
ssh-keygen -t rsa -f ./key_project
ssh -i key_project jesus@<instance_external_ip>
```
A storage site is created with 50GB and interconnected to the htc-instance through Google Cloud. Then, next firewall entry rules are configured:
1. Transmission Control Protocol (TCP) for 0 - 65535 ports, so the nodes are able to communicate between them through HTCondor, and to share a volume through the Network File System server (NFS).
2. Internet Control Message Protocol (ICMP) for all ports, so the ping requests are allowed.
3. TCP for 22 port, so the Secure Shell (SSh) is allowed.

![image](https://github.com/jesusch10/bdp1-project/assets/136498796/1b4b9ff4-4c6f-465b-8f75-24a9c7894c9c)

```
sudo su                       # Become superuser
fdisk /dev/sdb                # Access the partition menu and type commands: p, n, p (keep defaults), w
mkfs.ext4 /dev/sdb1           # Create the ext4 filesystem
mkdir /data2                  # Create a mountpoint for the new filesystem
vi /etc/fstab                 # Edit the fstab file to add this line: /dev/sdb1     /data2  ext4 defaults 0 0
mount -a                      # Mount all the filesystem listed in the fstab file
chmod 777 /data2/             # Change the permissions so the master and the nodes can read, write, and execute in the volume
```
## 2.2 Installing the NFS server:
In the htc-instance:
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
vim /etc/exports             # Add this line: /data2  <private IP of the slave-1 instance (client)>(rw,sync,no_wdelay)
exportfs -r
```
Display the NFS status with `systemctl status nfs`:

![image](https://github.com/jesusch10/bdp1-project/assets/136498796/19d229ac-a4b1-459c-9fa4-5bee67d5a851)

In the slave-1 instance:
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

## 2.3 Installing HTCondor dependencies and packages:
Both in htc-instance and slave-1 instance:
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
systemctl restart condor
systemctl enable condor
```
Display the HTCondor status with `systemctl status condor`:

![image](https://github.com/jesusch10/bdp1-project/assets/136498796/4213f34b-671f-4423-adf1-e480c6c2ffa9)

The slave-2 instance is created in Google Cloud as an image of the slave-1 image. Then the private IP slave-2 instance is added to the exports file of the htc-instance (server):
```
vim /etc/exports                      # Add this line: /data2  <private IP of the slave-2 instance (client)>(rw,sync,no_wdelay)
exportfs -r
```
Finally, the command `mount -a` is run in the slave-2 instance.






