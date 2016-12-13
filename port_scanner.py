#!/usr/bin/env python

from netaddr import IPSet
import socket
import traceback

__author__ = "Rakesh Reddy (rkreddy46@gmail.com)"
__version__ = 1.0

# This is a simple implementation of port scanner in python. It checks each IP one after another sequencially.
# A multi-processed version will be released soon.

# Set the default timeout for creating a connection. You need to change this based on the network delay
socket.setdefaulttimeout(2.0)

# This is the superset of IPs, you only want to use this if you want to cover all the IPs in the cloud
ipv4_addr_space = IPSet(['0.0.0.0/0'])

# Creating a set of private IPs to exclude
private = IPSet(['10.0.0.0/8', '172.16.0.0/12', '192.0.2.0/24', '192.168.0.0/16', '239.192.0.0/14'])

# Creating a set of reserved IPs to exclude
reserved = IPSet(['225.0.0.0/8', '226.0.0.0/7', '228.0.0.0/6', '234.0.0.0/7', '236.0.0.0/7', '238.0.0.0/8',
                  '240.0.0.0/4'])

# Create a superset of the private and the reserved IPs to exclude later on
unavailable = reserved | private

# Getting a list of public IPs
available = ipv4_addr_space ^ unavailable

# Here I am looking for an open 25 port (SMTP), you can always change this
port_to_check = 25
free_smtp = []

# I will be using this small subset for demo purposes instead of the superset of all valid IPs
test_ip_set = IPSet(['172.17.11.0/24'])

# The below line is commented because I am not going to scan the public IP addresses. But if you think it is legal in
# your state, you can use the "available" object to scan the public IPs. For now, I am only scanning a small subset
# for cidr in available.iter_cidrs():
for cidr in test_ip_set.iter_cidrs():
    for each_ip in cidr[1:-1]:
        try:
            # Core logic of opening a socket for each ip
            remote_server_ip = socket.gethostbyname(str(each_ip))
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((remote_server_ip, port_to_check))
            # If result is 0, then it means that the port is open
            if result == 0:
                print "IP address with open port 25: %s" % each_ip
                free_smtp.append(each_ip)
            else:
                print "IP not open: %s" % each_ip
            sock.close()
        except Exception as err:
            print "Exception seen - %s" % err
            print traceback.print_exc()
            continue
