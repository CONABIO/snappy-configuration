# snappy-configuration
This repository contains instructions and commands to configure snappy in a fresh linux environment.
In general, we are folliwing this [instructions](https://senbox.atlassian.net/wiki/spaces/SNAP/pages/50855941/Configure+Python+to+use+the+SNAP-Python+snappy+interface). It is important to said that snappy works with python 3.4, any other superior python version is not supported. 

# Anaconda download
First, it is necessary to download the files that we are going to use in the virtual environment and snappy package configuration. 
We will use [anaconda](https://www.anaconda.com/distribution/) to manage the virtual environment and install the necessary dependencies. 

From a web browser, go to the Anaconda distribution page, available at the following link:
``` 
https://www.anaconda.com/distribution/
```

In a terminal window type as a sudo user, not root:
``` bash
cd /tmp
curl -O https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
```

# Anaconda install
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
conda create -n snapp_env python=3.4 -c conda-forge
conda activate snappy_env
```

# Snappy download and install
We download and install the snappy package. We can get snappy from [ESA](https://step.esa.int/main/download/snap-download/) download page .
``` 
curl -O http://step.esa.int/downloads/7.0/installers/esa-snap_sentinel_unix_7_0.sh
bash esa-snap_sentinel_unix_7_0.sh
```

output
```
Unpacking JRE ...
Preparing JRE ...
Starting Installer ...
This will install ESA SNAP on your computer.
OK [o, Enter], Cancel [c]
``` 
press ENTER, after other configurations, SNAP instalation tool will ask, 

``` 
Which components should be installed?
*: SNAP [*1]
2: Sentinel-1 Toolbox [*2]
3: Sentinel-2 Toolbox [*3]
4: Sentinel-3 Toolbox [*4]
5: Radarsat-2 Toolbox [*5]
(To show the description of a component, please enter one of *1, *2, *3, *4, *5)
Please enter a comma-separated list of the selected values or [Enter] for the default selection:
```
press `2`, then ENTER until installer asks:

```
Which is your preferred Python version?

If you are a Python developer, you can use the SNAP Java API from Python or
you can even develop SNAP processor plugins using Python. Here you can
specify your preferred Python version by the given Python executable to be
used. Only Python versions 2.7, 3.3 and 3.4 are supported.
Configure SNAP for use with Python?
Yes [y], No [n, Enter]
```
type `y` and provides full python executable path, in this case 
```
/home/ubuntu/anaconda3/envs/snappy_env/bin/python
```

``` bash
cd snap/bin/
./snappy-conf /home/ubuntu/anaconda3/envs/snappy_env/bin/python
```

output

```
Configuring SNAP-Python interface...
Done. The SNAP-Python interface is located in '/home/ubuntu/.snap/snap-python/snappy'
When using SNAP from Python, either do: sys.path.append('/home/ubuntu/.snap/snap-python')
or copy the 'snappy' module into your Python's 'site-packages' directory.
```

# Test 

Now, we can check in a python console

```python
import sys
sys.path.append('/home/ubuntu/.snap/snap-python')
import snappy
```
or copy the 'snappy' module into your Python's 'site-packages' directory, that means

```
cp -r /home/ubuntu/.snap/snap-python/snappy /home/ubuntu/anaconda3/envs/snappy_env/lib/python3.4/site-packages
```

# Tunning

We need to specify the ram memory that snappy will use
```
cd /home/ubuntu
vi .snap/snap-python/snappy/snappy.ini
```

We change `java_max_mem: 1G` with `java_max_mem: 30G`. Preprocessing sentinel-1 images requires a large amount of memory, so it is important to set it to 30 Gb.

# Download Sentinel-1 data

Using [`sentinelsat`](https://sentinelsat.readthedocs.io/en/stable/) it's possible to query for products with python:

```python
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date

api = SentinelAPI('user', 'password','https://scihub.copernicus.eu/dhus')

# search region
footprint = geojson_to_wkt(read_geojson('./study_area_latlon.geojson'))

products = api.query(footprint,
                     date = ('20130101', '20151201'),
                     platformname = 'Sentinel-1',
                     orbitdirection = 'ascending',
                     polarisationmode = 'VV VH',
                     producttype = 'GRD',
                     sensoroperationalmode = 'IW')

print(products)

print(len(products))

api.download_all(products)
```

Check this [methodology](https://thegeoict.com/blog/2019/08/22/processing-sentinel-1-sar-images-using-snappy-snap-python-interface/). May be useful

