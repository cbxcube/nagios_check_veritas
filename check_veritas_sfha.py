#!/usr/bin/env python
##################################################################################################
# Nagios check_veritas_sfha.py
#
# Description:
# ------------
# With this little Python script you have the ability to check your Veritas servicegroups and
# the status of your volumegroup. Please use ./check_veritas_sfha.py -h to get an overview of
# the needed parameters. 
# In all cases you need the exact name of the servicegroup which is shown by the output of 
# /opt/VRTS/bin/hastatus -sum and of course you need the exact name of the volumegroup.
#
#
# Author:               Frank Reimer
# Version:              0.3
# Creation Date:        2012-08-09
# --------------------------------------------------
#
# Version History:
#
# 2012-08-14: Fixing servicegroup check - removing re.compile for Python compatibility
# 2012-08-10: Adding check for plexes in volumegroup
# 2012-08-09: Script creation
#
##################################################################################################
# README:
#
# If you want to use this script, your Nagios user needs sudo privileges to perform this script.
# Start visudo and add the following lines at the end of the file:
#
# <nagiosuser> ALL=(ALL) NOPASSWD:/opt/VRTS/bin/hastatus
# <nagiosuser> ALL=(ALL) NOPASSWD:/sbin/vxprint
# <nagiosuser> ALL=(ALL) NOPASSWD:/<path>/<to>/check_veritas_status.py
#
# Tested with the following Python versions:
# - 2.4.3
# - 2.6.6
##################################################################################################

# Adding script version
script_version=str(0.3)

# Importing some modules
import os
import re
import sys
import platform
import commands
import subprocess
from optparse import OptionParser

# Defining some global variables
CHECK_VOL_STATUS_CRITICAL=0
HASUMCMD='/opt/VRTS/bin/hastatus -sum'
VXPRINTCMD='/sbin/vxprint -g'

# Define some global status

SG_STATUS=[]
VG_STATUS=[]

# Getting options

### Defining some options for OptionParser
parser = OptionParser(usage="%prog [-s <SERVICEGROUP>] [-v <VOLUMEGROUP>]", version="%prog " + script_version)
parser.set_defaults(verbose=False)
parser.add_option("-s", "--servicegroup", dest="servicegroup", help="Servicegroup you want to monitor.")
parser.add_option("-v", "--volumegroup", dest="volumegroup", help="Volumegroup you want to monitor")
(options, args) = parser.parse_args()
if not (options.servicegroup or options.volumegroup):
        parser.error("Missing Option. Please use option -h")
if (options.servicegroup and options.volumegroup):
        parser.error("Please only provide ONE parameter.")

def CHECK_SERVICEGROUP(SG):
    OFFLINE=0
    SG_REGEX=r"%s\s" % SG
    CHECK_SG=os.popen(HASUMCMD)
    CHECK_SG_PRINTOUT=[line.strip() for line in CHECK_SG]
    for LINE in CHECK_SG_PRINTOUT:
        #if re.search(re.compile(SG), LINE, re.I) and re.search(r"ONLINE", LINE, re.I):
        if re.search(SG_REGEX, LINE, re.I) and re.search(r"ONLINE", LINE, re.I):
            str_SG_STATUS=str("OK: Servicegroup " + SG + " is online on host " + LINE.split(" ")[7])
            SG_STATUS.append(str_SG_STATUS)
        #if re.search(re.compile(SG), LINE, re.I) and re.search(r"PARTIAL", LINE, re.I):
        if re.search(SG_REGEX, LINE, re.I) and re.search(r"PARTIAL", LINE, re.I):
            str_SG_STATUS=str("WARNING: Servicegroup " + SG + " is in partial state on host " + LINE.split(" ")[7])
            SG_STATUS.append(str_SG_STATUS)
        #if re.search(re.compile(SG), LINE, re.I) and re.search(r"OFFLINE", LINE, re.I):
        if re.search(SG_REGEX, LINE, re.I) and re.search(r"OFFLINE", LINE, re.I):
            OFFLINE=OFFLINE+1
            if OFFLINE > 1:
                str_SG_STATUS=str("CRITICAL: Servicegroup " + SG + " is offline on all hosts.")
                SG_STATUS.append(str_SG_STATUS)

def CHECK_VOLUMEGROUP(VG):
    CHECK_VG_CMD=VXPRINTCMD + " " + VG
    CHECK_VG=os.popen(CHECK_VG_CMD)
    CHECK_VG_PRINTOUT=[line.strip() for line in CHECK_VG]

    for LINE in CHECK_VG_PRINTOUT:
        if re.search(r"pl ", LINE, re.I):
                if LINE.split()[3] == "ENABLED" and LINE.split()[6] == "ACTIVE":
                        str_VG_STATUS=str("OK: Plex " + LINE.split()[1] + " is clean.")
                        VG_STATUS.append(str_VG_STATUS)
                else:
                        str_VG_STATUS=str("CRITICAL: Plex " + LINE.split()[1] + " is unclean.")
                        VG_STATUS.append(str_VG_STATUS)

if (options.servicegroup):

    CHECK_SERVICEGROUP(options.servicegroup)
    for j in SG_STATUS:
            if j.split(":")[0] == "OK":
                    print j.split(":")[0] + ":" + j.split(":")[1]
                    sys.exit(0)
            if j.split(":")[0] == "WARNING":
                    print j.split(":")[0] + ":" + j.split(":")[1]
                    sys.exit(1)
            if j.split(":")[0] == "CRITICAL":
                    print j.split(":")[0] + ":" + j.split(":")[1]
                    sys.exit(2)

    if not CHECK_SERVICEGROUP(options.servicegroup):
        print "UNKOWN: Servicegroup " + options.servicegroup + " is unkown."
        sys.exit(3)

if (options.volumegroup):
    CHECK_VOLUMEGROUP(options.volumegroup)
    for k in VG_STATUS:
        if k.split(":")[0] == "OK":
                print VG_STATUS
                sys.exit(0)
        if k.split(":")[0] == "CRITICAL":
                print VG_STATUS
                sys.exit(2)

    if not CHECK_VOLUMEGROUP(options.volumegroup):
        print "UNKOWN: Volumegroup " + options.volumegroup + " is unkown."
        sys.exit(3)
