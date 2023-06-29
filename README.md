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

