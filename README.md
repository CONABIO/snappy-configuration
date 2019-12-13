# snappy-configuration
 This repository contains instructions and commands to configure snappy in a fresh linux environment.

# Downloads
First, it is necessary to download the files that we are going to use in the virtual environment and snappy package configuration. 
We will use [anaconda](https://www.anaconda.com/distribution/) to manage the virtual environment and install the necessary dependencies there and we can get snappy from [ESA](https://step.esa.int/main/download/snap-download/) download page .

In a terminal window type as a sudo user, not root:
``` bash
cd /tmp
curl -O wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
```

Check the integrity of the installer with a cryptographic hash check using the SHA-256 checksum:

```bash
sha256sum Anaconda3-2019.10-Linux-x86_64.sh
```
output:
``` bash
09f53738b0cd3bb96f5b1bac488e5528df9906be2480fe61df40e0e0d19e3d48  Anaconda3-5.2.0-Linux-x86_64.sh
```

```
bash Anaconda3-2019.10-Linux-x86_64.sh
```

You will receive the following result to review the license agreement by pressing ENTER until the end.
```
Welcome to Anaconda3 5.2.0

In order to continue the installation process, please review the license
agreement.
Please, press ENTER to continue
>>>
...
Do you approve the license terms? [yes|no]
```


Once you accept the license, you will be asked to select the installation location. You can press ENTER to accept the default location or specify a different location.

```
Output
Anaconda3 will now be installed into this location:
/home/ubuntu/anaconda3

  - Press ENTER to confirm the location
  - Press CTRL-C to abort the installation
  - Or specify a different location below

[/home/ubuntu/anaconda3] >>>
```


When the installation is complete, you will receive the following result:
```
...
installation finished.
Do you wish the installer to prepend the Anaconda3 install location
to PATH in your /home/sammy/.bashrc ? [yes|no]
[no] >>> 
```

It is recommended that you type `yes` to use the `conda` command.

Now, you can activate the installation with the following command:

```
source ~/.bashrc
```

Use the conda command to test the installation and activation:
```
conda list
```

Now, we can create our virtual environment

```
conda create -n snappy_env python=3.6 anaconda
source activate snappy_env
```
 
