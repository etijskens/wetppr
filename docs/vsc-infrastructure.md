# VSC infrastructure

## Applying for a guest account (students)

!!! Note
    The project work (see [Evaluation](evaluation)) requires access to one of the university's HPC clusters. If you
    do not already have a VSC account, you must create a SSH public/private key pair (see below how to do that) and
    send it by e-mail to franky.backeljauw@uantwerpen.be with engelbert.tijskens@uantwerpen.be in cc. A
    ***guest account*** will subsequently be created for you .

## Applying for a VSC account (researchers from Flanders)

See [Getting acces to VSC clusters](https://docs.vscentrum.be/en/latest/access/getting_access.html).

## Create an ssh public/private key pair

A ssh public/private key pair is a way for secure access to a system through the Secure Shell protocol. They are
basically two small files with matching numbers. You may think of the public key as a lock. Everyone may see the
lock but no one can open the lock without the key, which is the private part of the key pair. The public key
(the lock) will be placed on a system you need access to, in this case the Tier-2 supercomputer of our university
(currently, that is [Vaughan](https://docs.vscentrum.be/en/latest/antwerp/tier2_hardware/vaughan_hardware.html?
highlight=vaughan)). To access to the supercomputer (that is, open the lock) from, say, your laptop, your need the
private key to be stored on your laptop (or a USB memory stick) and pass it to the SSH protocol which will verify
the private key and the public key match and, in case they do, open the lock and grant you access.

To create a ssh public/private key pair proceed as follows.

### On Windows

Open`powershell` or `cmd`, and type the following command:

```bash
> ssh-keygen -t rsa -b 4096
```

You will then be prompted for a file location. You may accept the default location by entering. If the files already
exist you can choose to overwrite them or to cancel the operation.

```
Enter file in which to save the key (C: \Users \your_username/ .ssh/id rsa) :
C:\Users\your_username/.ssh/id rsa already exists.
Overwrite (y/n)? y
```

You will then be prompted for a passphrase to provide an extra level of protection for in case somebody would steal the
private key. Press enter for an empty passphrase.

```
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
```

Finally you will be notified of where the keys are stored:  

```
Your identification has been saved in C: \Users\your_username/.ssh/id rsa.
Your public key has been saved in C: \Users\your_username/.ssh/id rsa.pub.
```

!!! Note
    To obtain a guest account students must send their ***public*** key (and only their public key, the private key
    is, well, um, private) to franky.backeljauw@uantwerpen.be with engelbert.tijskens@uantwerpen.be in _cc_. The
    public key is the one with the `.pub` extension.

### On Linux and MacOS

Open a terminal, and type the following command:

```bash
> ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_vsc
```

The name `id_rsa_vsc` is arbitrary, but is best chosen to be meaningfull. You will be prompted for a passphrase to
provide an extra level of protection for in case somebody would steal the private key. Press enter for an empty
passphrase.

```bash
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
```

Finally, you will be notified of the files (=keys) created:

```bash
Your identification has been saved in /home/user/.ssh/id_rsa_vsc
Your public key has been saved in /home/user/.ssh/id_rsa_vsc.pub
```

!!! Note
    To obtain a guest account students must send their ***public*** key (and only their public key, the private key
    is, well, um, private) to franky.backeljauw@uantwerpen.be with engelbert.tijskens@uantwerpen.be in _cc_. The
    public key is the one with the `.pub` extension.
