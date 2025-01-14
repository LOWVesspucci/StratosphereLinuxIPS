# Usage

Slips can read the packets directly from the **network interface** of the host machine, and packets and flows from different types of files, including

- Packet capture (pcap)
- Argus binetflow
- Zeek/Bro folder with logs, or logs separately 
- Nfdump flows

After Slips was run on the traffic, the Slips output can be analyzed with Kalipso GUI interface. In this section, we will explain how to execute each type of file in Slips, and the output can be analyzed with Kalipso.

## Reading the input

The table below shows the commands Slips uses for different inputs. The first part of the command **./slips.py -c slips.conf** is same, the second part changes depending on the input type. Also, the user can execute **./slips.py --help** to find correct argument to run Slips on each type of the file.

<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>


<table>
  <tr>
    <th>File/interface</th>
    <th>Slips Argument</th>
    <th>Example command</th>
  </tr>
  <tr>
    <td>Network interface (*)</td>
    <td>-i</td>
    <td>./slips.py -c slips.conf -i en0</td>
  </tr>
  <tr>
    <td>pcap</td>
    <td>-r</td>
    <td>./slips.py -c slips.conf -r test.pcap</td>
  </tr>
  <tr>
    <td>Argus binetflow</td>
    <td>-f</td>
    <td>./slips.py -c slips.conf -f test.binetflow</td>
  </tr>
  <tr>
    <td>Zeek/Bro folder/log</td>
    <td>-f</td>
    <td>./slips.py -c slips.conf -f zeek_files</td>
  </tr>
  <tr>
    <td>Nfdump flow</td>
    <td>-b</td>
    <td>./slips.py -c slips.conf -b test.nfdump </td>
  </tr>
  </table>

(*) To find the interface in Linux, you can use the command ```ifconfig```.


There is also a configuration file **slips.conf** where the user can set up parameters for Slips execution and models separately. Configuration of the **slips.conf** is described [here](#modifying-a-configuration-file).

## Reading the output
The output process collects output from the modules and handles the display of information on screen. Currently, Slips' analysis and detected malicious behaviour can be analyzed as following:

- **Kalipso** - Node.JS based graphical user interface in the terminal. Kalipso displays Slips detection and analysis in colorful table and graphs, highlighting important detections. See section Kalipso for more explanation.
- **alerts.json and alerts.txt in the output folder** - collects all evidences and detections generated by Slips in a .txt and .json formats.
- **log files in a folder _current-date-time_** - separates the traffic into files according to a profile and timewindow and summarize the traffic according to each profile and timewindow.

There are two options how to run Kalipso:
1. You can run Kalipso as a shell script in another terminal using the command:

	```./kalipso.sh```
2. Use the argument ```-G```  when execting Slips. Example:

	``` ./slips.py -c slips.conf -i wlp3s0 -G ```

## Modifying a configuration file

Slips has a ```slips.conf``` the contains user configurations for different modules and general execution. Below are some of Slips features that can be modifie with respect to the user preferences.

### Generic configuration

**Time window width.**

Each IP address that appears in the network traffic of the input is represented as a profile in Slips. Each profile is divided into time windows. Each time window is 1 hour long by default, and it gathers the network traffic and its behaviour for the period of 1 hour. The duration of the timewindow can be changed in the the slips.conf using

```time_window_width```

**Log files.**
To disable the creation of log files, there are two options:
1. Running Slips with ```-l``` flag. 
2. Setting ```create_log_files``` to ```no```.

You can also change how often Slips creates log files using the ```log_report_time``` variable.

### Disabling module
You can disable modules easily by appending the module name to the ```disable``` list.

### ML Detection

The ```mode=train``` should be used to tell the MLdetection1 module that the flows received are all for training.

The ```mode=test``` should be used after training the models, to test unknown data. 

You should have trained at least once with 'Normal' data and once with 'Malicious' data in order for the test to work.

### VirusTotal

In order for virustotal module to work, you need to add your VirusTotal API key to the file
```modules/virustotal/api_key_secret```.

You can specify the path to the file with VirusTotal API key in the ```api_key_file``` variable.

The file should contain the key at the start of the first line, and nothing more.

If no key is found, virustotal module will not start.

### Threat Intelligence
The threat intelligence module reads IoCs from local and remote files. 

**Remote files**

We update the remote ones regularly. The list of remote threat intelligence files is set in the variables ```ti_files``` variable in slips.conf. You can insert your own remote threat intelligence files in this variable. Supported extensions are: .txt, .csv, .netset, ipsum feeds, or .intel.
 
The remote files are installed to the path set in the ```download_path_for_local_threat_intelligence```. By default, the files are stored in the Slips directory ```modules/ThreatIntelligence1/remote_data_files/``` 

**Local files**

You can insert your files into the folder specified in the variable ```download_path_for_remote_threat_intelligence```. You can also hardcode your own malicious IPs in the file```modules/ThreatIntelligence1/local_data_files/own_malicious_ips.csv```

### Flowalerts

Slips needs a threshold to determine a connection of a long duration. By default, it is 1500 seconds, and it can be changed in the variable ```long_connection_threshold```

### Exporting Alerts

Slips can export alerts to Slack and STIX.

To specify where to export, you can append the ```export_to``` list. 

**To export to Slack**

You need to add your Slack bot token to the file ```modules/ExportingAlerts/slack_bot_token_secret```. The file should contain the token at the start of the first line, and nothing more.

If you do not have a Slack bot, follow steps 1 to 3 [here](https://api.slack.com/bot-users#creating-bot-user) to get one.

You can specify the channel name to send alerts to in the ```slack_channel_name``` variable, and the sensor name to be sent together with the alert in the ```sensor_name``` variable.

**To export to STIX**

If you want to export alerts using Stix, change ```export_to``` variable to export to STIX, and Slips will automatically generate a 
```STIX_data.json``` containing all alerts it detects.

You can add your TAXII server details in the following variables:

```TAXII_server```: link to your TAXII server

```port```: port to be used

```use_https```: use https or not.

```discovery_path``` and ```inbox_path``` should contain URIs not full urls. For example:

```python
discovery_path = /services/discovery-a
inbox_path = /services/inbox-a
```

```collection_name```: the collection on the server you want to push your STIX data to.

```push_delay```: the time to wait before pushing STIX data to server (in seconds). It is used when slips is running non-stop (e.g with -i )

```taxii_username```: TAXII server user credentials

```taxii_password```: TAXII server user password

```jwt_auth_url```: auth url if JWT based authentication is used.

If running on a file not an interface, Slips will export to server after analysis is done. 
