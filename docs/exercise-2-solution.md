# Exercise 2 - Transfer your local project to a VSC cluster

## 1. Cloning a remote GitHub repo

First, login on Vaughan (Check out the VSC documentation on
[this](https://docs.vscentrum.be/en/latest/access/access_and_data_transfer.html#logging-in-to-a-cluster)
).

### Logging in on Vaughan

Open a terminal and execute the command:

```shell
> ssh <your_vsc_id>@login-vaughan.hpc.uantwerpen.be
Last login: Mon Aug 14 14:25:17 2023 from 81.164.139.192

--------------------------------------------------------------------

Welcome to VAUGHAN !

Vaughan specific links:
  https://docs.vscentrum.be/en/latest/antwerp/tier2_hardware/vaughan_hardware.html
  https://docs.vscentrum.be/en/latest/antwerp/SLURM_UAntwerp.html

General links:
  https://docs.vscentrum.be/en/latest/antwerp/tier2_hardware.html
  https://docs.vscentrum.be
  https://www.uantwerpen.be/hpc

Questions or problems? Do not hesitate and contact us:
  hpc@uantwerpen.be

Happy computing!

--------------------------------------------------------------------

Your quota is:

file system /data/antwerpen
    using 95.77G of 250G space, 311062 of 500k files
file system /user/antwerpen
    using 494.4M of 3G space, 2463 of 20k files
file system /scratch/antwerpen
    using 382.1G of 2T space, 57803 of 250k files

--------------------------------------------------------------------
>
```

Which one of the (currently) two login nodes of Vaughan you will land on, is rather random. You can
explicitly ask for a login node:

```shell
> ssh <your_vsc_id>@login1-vaughan.hpc.uantwerpen.be
```

or

```shell
> ssh <your_vsc_id>@login2-vaughan.hpc.uantwerpen.be
```

After logging in you will receive information about

  * the last time you logged in
  * some links with information
  * information on your file quota on `/data/antwerpen`, `/user/antwerpen` and `/scratch/antwerpen`

The latter is especially important. You have access to 3 file spaces: data, user (or home) and
scratch.

  * user file space is small and backed up. It is intended for configuration files.
  * data file space is large, backed up, but has slower access than scratch. This is the place to:
     * store your own Python projects
     * install Python packages not installed on Vaughan by the VSC user support team

  * scratch file space is large, fast, but not backed up.

On each of these file spaces you can use a limited amount of disk space and a limited number of
files. _E.g._ my data file space allows for 250G (97.55G occupied) and 500 000 files (I have already
311062 files). When you install your own software components the number of files rises quickly.
When your file quota are exceeded for aa file space, you will still be able to login, but any proces
that tries to create a file will fail. Sometimes the cause of failure is not immediately clear.
_E.g._ a submitted job may fail when attempting to create an output file. Or, connecting to the
cluster with [vscode]() will fail because it installs a `.vscode-server` every time, and it cannot
due to `file quota eceeded`.

!!! Tip
    Check the file quota message on every login.

### Cloning a GitHub repo

As explained above, it is best to clone the remote repo on the data file space

```shell
> cd $VSC_DATA
> pwd
/data/antwerpen/201/vsc20170
```

Make a workspace directory for all our projects
```shell
> mkdir workspace
> cd workspace
> pwd
/data/antwerpen/201/vsc20170/workspace
```
Clone my Dot repo (_e.g._):

```shell
> git clone https://github.com/etijskens/Dot.git
Cloning into 'Dot'...
remote: Enumerating objects: 55, done.
remote: Counting objects: 100% (55/55), done.
remote: Compressing objects: 100% (34/34), done.
remote: Total 55 (delta 15), reused 52 (delta 12), pack-reused 0
Receiving objects: 100% (55/55), 16.82 KiB | 1.29 MiB/s, done.
Resolving deltas: 100% (15/15), done.
```

To work with the project, `cd` into the project directory:

```shell
> cd Dot
> pwd
/data/antwerpen/201/vsc20170/workspace/Dot
```

As `Dot` is a `wip` project we must make Python available first:
```shell
> module load Python
> wip info
Project    : Dot: dot product implementations
Version    : 0.0.0
Package    : dot
GitHub repo: --
Home page  : --
Location   : /data/antwerpen/201/vsc20170/Dot
docs format: Markdown
```

## 2. Repeat all the timings of [Exercise 1](exercise-1.md)

When you login on the cluster, you land on a ***login node***, together with many other users that are
logged in. That makes it a crowded place. Although you can run commands, commands taking longer than
a minute, may need to share resources with other users, making it slower than on your personal
machine. Timing tests are therefor not always reliable when run on a login node. The login node is
your point of access for manipulating files and setting up the work, but the real number crunching
is to happen on the compute nodes, of which there are far more than login nodes. Compute nodes must
be reserved by you in a ***job script***. The job script

* requests the resources needed for the job,
* sets up the system environment for the job,
* specifies the command(s) to be executed.

Details are described in [VSC infrastructure/Submitting jobs on Vaughan][submitting-jobs-on-vaughan]

## 3. Add the timings to the `README.md` file and explain your observations

Compare the timings from the compute node with those on our own machine, Do you notice any
differences?
