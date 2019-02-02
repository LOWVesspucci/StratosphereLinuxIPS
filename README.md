# Stratosphere Linux IPS (slips) Version 0.5
This is the new version of the Stratosphere IPS, a behavioral-based intrusion detection and prevention system that uses machine learning algorithms to detect malicious behaviors. It is part of a larger suite of programs that include the [Stratosphere Windows IPS] and the [Stratosphere Testing Framework].


## Architecture of operation
[rewrite]
- The data collected and used is on the _profile_ level and up. Slips does not work with data at the _flow_ level or _packet_ level to classify. This means that the simplest data structure available inside slips is the profile of an IP address. The modules can not access individual flows.


## Install

### Dependencies
- python3.6 or greater
- py37-redis (Be sure that you install the redis libraries for your python3 version. This can be done with pip3, but your 'python3' executable in your path should point to the version of python you are using, such as python3.7)
- redis database

#### Installing dependencies    
The new version of slips uses redis as a backend database, so you need to have redis running.

1. Start Redis
    - In Linux
        - As a daemon
            The easiest way to launch Redis as a daemon is to edit the configuration file and change the following line:

            ```
            # By default Redis does not run as a daemon. Use 'yes' if you need it.
            # Note that Redis will write a pid file in /var/run/redis.pid when daemonized.
            daemonize yes
            ```

            You can also use:

            ```
            redis-server --daemonize yes
            ```

    - In macos
        - As a deamon

            ```
            sudo port load redis
            ```
        - By hand and leaving redis running on the console

            ```
            redis-server /opt/local/etc/redis.conf
            ```

2. Argus
Currently only Flows generated by Argus are read, but we will expand this soon.

If you don't have an Argus instance to generate your own flows, first install it:
    - Source install from [Argus].
    - In Debian and Ubuntu you can do:

        ```
        sudo apt-get install argus argus-clients
        ```

To run argus in your own computer you should do:

    ```
    argus -B localhost -F [slipsfolder]/argus.conf
    ```

## Usage
Slips can be used by passing flows in its stdin, like this:

    ```
    cat test-flows/test3.binetflow | ./slips.py -l -c slips.conf -v 2 
    ```

Or it can be told to open a certain file, like this:

    ```
    ./slips.py -r test-flows/test3.binetflow -l -c slips.conf -v 2 
    ```

To read your own packets you can do:

    ```
    sudo argus -i eth0 -S 5 -w - |ra -n -r -  | ./slips.py -l -v 2 -c slips.conf
    ```

    Which means run argus in eth0, report flows every 5s, give them to ra, ra only prints the flows, and slips works with them.



## Detection Models
[rewrite]
The core of the slips program is not only the machine learning algorithm, but more importantly the __behavioral models__. The behavioral models are created with the [Stratosphere Testing Framework] and are exported by our research team. This is very important because the models are _curated_ to maximize the detection. If you want to play and create your own behavioral models see the Stratosphere Testing Framework documentation.

The behavioral models are stored in the __models__ folder and will be updated regularly. In this version you should pull the git repository by hand to update the models.


## Features 
[rewrite]
This version of slips comes with the following features:

- If you execute slips without the -m parameter it will __not__ detect any behavior in the network but just print the tuples (see the Stratosphere web page for more information). So actually you can also use slips to see what is happening in your network even without detection.
- Use -a to restrict the minimum amount of letters that the tuples had to have to be considered for detection. The default is a minimum of 3 letters which is enough for having at least one periodic letter.
- slips works by separating the traffic in time windows. This allows it to report to the user the detections in a fixed amount of time. The default time window is now __1 minute__ but you can change it with the parameter -w (a time window of five minutes is also recommended). (Warning: In the future we will update this to also consider the detection of IP addresses instead of tuples)
- If you want to tell slips to actually try to detect something, you should specify -m to tell slips where to find the behavioral models.
- The -p option tells slips to print the tuples that were detected. Even if the detection is working, without -p the tuples are not printed.
- If you want to be alerted of any detection without looking at the screen you can specify -s to have a sound alert. You need to install the pygames libraries.
- If you want to avoid doing any detection you should use -D.
- If you want to anonymize the source IP addresses before doing any processing, you can use -A. This will force all the source IPs to be hashed to MD5 in memory. Also a file is created in the current folder with the relationship of original IP addresses and new hashed IP addresses. So you can later relate the detections.



## The use of verbose (-v)
[rewrite]



### Where does it work
[rewrite]
- Slips runs in 
    - Ubuntu 16.04 LTS
    - Debian stable/testing/unstable
    - MacOS 10.9.5, 10.10.x to 10.12.x
- To try:
    - Android
    - IOS


### Roadmap
[rewrite]

### Changelog
[rewrite]
- 0.5 Completely renewed architecture and code.
- 0.4 was never reached
- 0.3.5
- 0.3.4
    - This is a mayor version change. Implementing new algorithms for analyzing the results, management of IPs, connections, whois database and more features.
    - A new parameter to specify the file (-r). This is as fast as reading the file from stdin.
    - Now we have a configuration file slips.conf. In there you can specify from fixed parameters, the time formats, to the columns in the flow file.
- 0.3.3alpha
    - First stable version with a minimal algorithm for detecting behavioral threats.



### Author and Contributors
[rewrite]

- The author of the project is Sebastian Garcia. sebastian.garcia@agents.fel.cvut.cz, eldraco@gmail.com. (Send an email for bugs, reports, ideas or comments)
- Ondrej Lukas: New detection metric of infected IPs based on timewindows, detection windows, weighted scores and averages. Also all the ip_handler, alerts classes, etc.
- Elaheh Biglar Beigi
- MariaRigaki 
- kartik88363
- arkamar


[Argus]: http://qosient.com/argus/ "Argus"
[Stratosphere Testing Framework]: https://github.com/stratosphereips/StratosphereTestingFramework
[Stratosphere Windows IPS]: https://github.com/stratosphereips/StratosphereIps
