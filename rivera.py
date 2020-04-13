#!/bin/python3

import os
import sys

if len(sys.argv) < 2:
	print("Usage\n")
	exit(0)
else:
	domain = sys.argv[1]


G, B, R, W, M, C, end = '\033[92m', '\033[94m', '\033[91m', '\x1b[37m', '\x1b[35m', '\x1b[36m', '\033[0m'
info = end + W + "[-]" + W
good = end + G + "[+]" + C
bad = end + R + "[" + W + "!" + R + "]"

print("#"*40)
print("Rivera")
print("#"*40)

#Aquatone Checking
#Change it to the Subprocess for clean output

aquatone_check = os.system("ls -al /usr/local/bin/ | grep -o 'aquatone'")

if aquatone_check:
	print(bad + "Please install aquatone\n")
	exit(0)

print(good + "Aquatone Found Continuing\n")
os.system("aquatone-discover -d %s" % domain)
print(good + "Aquatone Finished Processing\n")
print(good + "Making a directory for temporary working\n")
file = "hosts_%s.txt" % domain
print(good + "Creating a Temporary file to read from\n")
os.system("cat /root/aquatone/%s/hosts.txt | cut -d ',' -f 2 > /tmp/riv/%s" % (domain, file))
print(good + "Triggering Nmap\n")
file_path = "/tmp/riv/%s" % file
os.system("nmap -sS -iL %s -oA %s" % (file_path, domain))

os.system("cat %s.nmap | grep -B 1 'Host is up' | egrep '*\(*\)$' | awk '{print $6}' | cut -d '(' -f 2 | tr ')' ' ' > /tmp/riv/suphost.txt" % domain)
print(good + "Performing Basic Scans for the surely Up Host \n")
os.system("nmap -sV -sC -T4 /tmp/riv/suphost.txt -oA Final_Scan_%s -vv" % domain)
print(info + "Scans results are generated Final_Scan_%s.*\n" % domain)
print(info + "Removing all the temprory files\n")
os.system("rm -rf /tmp/riv/")
