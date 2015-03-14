# nagios_check_veritas
Nagios check_veritas_sfha.py

Description:
------------
With this little Python script you have the ability to check your Veritas servicegroups and
the status of your volumegroup. Please use ./check_veritas_sfha.py -h to get an overview of
the needed parameters. 
In all cases you need the exact name of the servicegroup which is shown by the output of 
/opt/VRTS/bin/hastatus -sum and of course you need the exact name of the volumegroup.


- Author:               Frank Reimer
- Version:              0.3
- Creation Date:        2012-08-09

Version History:

- 2012-08-14: Fixing servicegroup check - removing re.compile for Python compatibility
- 2012-08-10: Adding check for plexes in volumegroup
- 2012-08-09: Script creation

#PREREQUISITES:
If you want to use this script, your Nagios user needs sudo privileges to perform this script.
Start visudo and add the following lines at the end of the file:

<nagiosuser> ALL=(ALL) NOPASSWD:/opt/VRTS/bin/hastatus
<nagiosuser> ALL=(ALL) NOPASSWD:/sbin/vxprint
<nagiosuser> ALL=(ALL) NOPASSWD:/<path>/<to>/check_veritas_status.py

Tested with the following Python versions:
- 2.4.3
- 2.6.6

#USAGE:
Usage: check_veritas_sfha.py [-s <SERVICEGROUP>] [-v <VOLUMEGROUP>]

Options:
-  --version                                          show program's version number and exit
-  -h, --help                                         show this help message and exit
-  -s SERVICEGROUP, --servicegroup=SERVICEGROUP       Servicegroup you want to monitor.
-  -v VOLUMEGROUP, --volumegroup=VOLUMEGROUP          Volumegroup you want to monitor
