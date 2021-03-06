import paramiko
import re
import getpass
import time
import csv
import sys
import os
import difflib
import subprocess

def hostProperFormat(host_ip):
	splitted = re.split('\.', host_ip)

	if not len(splitted) == 4:
		return False

	else:
		for field in splitted:
			if not (0 <= int(field)) and (int(field) <= 255):
				return False
			else:
				continue
		return True

def validateHost(host_ip):
	while(not hostProperFormat(host_ip)):
		host_ip = raw_input("HOST IP: ")
	return host_ip

def get_user_pass():
	username = raw_input("Username: ")
	password = getpass.getpass()
	return [username, password]

def startConnection(host_ip, us, passw):
	validip = validateHost(host_ip)
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.load_system_host_keys()
	try:
		client.connect(hostname=host_ip, username=us, password=passw)
	except paramiko.AuthenticationException:
		print "Authentication failed."
	except paramiko.SSHException: 
		print "Could not connect to Host via SSH"
	try:
		channel = client.invoke_shell()
	except Exception:
		print "Error occured in starting shell"
	else:
		while(not channel.recv_ready()):
			pass
		print channel.recv(1000)
		print type(channel)
		channel.keep_this = client
		return channel

def input_receive_comm(channel, com):
	while not channel.send_ready():
		pass
	channel.send(com)
	time.sleep(0.3)
	output = channel.recv(5000)
	return output


def main():
	usage = "usage: %prog [options] hostname configfile tofile"
	parser = optparse.OptionParser(usage)
	parser.add_option("-p", action="store",	help="Password input")
	parser.add_option("-u", action="store", help="Username input")
	(options, args) = parser.parse_args(args)
	password = options.p
	username = options.u
	configfile = args[1]
	hostname = args[0]
	tofile = args[2]
	if hostProperFormat(hostname):
		try:
			channel = startConnection(hostname, username, password)
		except 

	
ipaddress = raw_input("HOST IP: ")

ipaddress = validateHost(ipaddress)
channel = startConnection(ipaddress)
print input_receive_comm(channel, "show ip int b\n")