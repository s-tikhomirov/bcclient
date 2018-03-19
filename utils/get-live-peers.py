#! /usr/bin/python3

import subprocess
import socket
import time
import re

def get_bootstrap_urls(filename):
	bootstrap_dns_entries = []
	with open(filename, 'r') as file:
		for line in file.read().splitlines():
			bootstrap_dns_entries.append(line)
	return bootstrap_dns_entries

def get_ips_from_dns(urls):
	ips = []
	for url in urls:
		for result in socket.getaddrinfo(url, 0, 0, 0, 0):
			ips.append(result[-1][0])
	ips = list(set(ips))
	return ips

def write_list_to_file(l, filename='peers.txt'):
	with open(filename, 'w') as file:
		file.write('# ' + str(int(time.time())) + ' 0\n')
		for elem in l:
			file.write(elem + '\n')

# copied from parser.py
def findIp(string):
	# Regexes taken from: https://gist.github.com/mnordhoff/2213179 (^ and $ excluded)
	ipv4_address = re.compile('(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])')
	ipv6_address = re.compile('(?:(?:[0-9A-Fa-f]{1,4}:){6}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|::(?:[0-9A-Fa-f]{1,4}:){5}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){4}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){3}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,2}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){2}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,3}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}:(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,4}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,5}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}|(?:(?:[0-9A-Fa-f]{1,4}:){,6}[0-9A-Fa-f]{1,4})?::)')
	maybeIpv4 = re.search(ipv4_address, string)
	if (maybeIpv4 is None):
		maybeIpv6 = re.search(ipv6_address, string)
		if maybeIpv6 is None:
			raise ValueError("A log string from a received message must contain an IP address." + string)
		return maybeIpv6
	return maybeIpv4

def get_addresses_from_peers(peers_filename, bcclient_path='../', timeout=15):
	lines = subprocess.check_output('timeout ' + str(timeout) + ' ./bcclient -f ' + peers_filename + ' -s getaddr -l addr | grep r:addr', 
		shell=True,
		cwd=bcclient_path).decode('utf-8').split('\n')
	ips = []
	for line in lines:
		try:
			ips.append(findIp(line).group(0))
		except ValueError:
			continue
	ips = list(set(ips))
	return ips

def is_accessible(response):
	return (('Version received' in response) and ('Verack received' in response))

def get_accessible_ips(peers_filename, bcclient_path='../', timeout=1):
	good_ips = []
	bad_ips = []
	lines = [line.rstrip('\n') for line in open(peers_filename, 'r')][1:] # skip '# <timestamp> 0'
	total_ips = len(lines)
	print("Total " + str(total_ips) + " IPs in file.")
	counter = 0
	for ip in lines:
		if (counter % 1 == 0):
			print("Checking IP " + str(counter) + " of " + str(total_ips))
		response = ''
		try:
			response = subprocess.check_output('timeout ' + str(timeout) + ' ./bcclient ' + ip, 
				shell=True,
				cwd=bcclient_path).decode('utf-8')
		except subprocess.CalledProcessError:
			pass	# ignore exit on timeout: peer is inaccessible
		if is_accessible(response):
			good_ips.append(ip)
		else:
			bad_ips.append(ip)
		counter += 1

	print(str(len(good_ips)) + ' accessible, ' + str(len(bad_ips)) + ' inaccessible IPs.')
	return good_ips


def main():
	path = '/home/sergei/Documents/code/bcclient/bcclient/utils/'
	bootstrap_urls_file = path + 'bootstrap-dns-bitcoin-testnet.txt'
	bootstrap_ips_file = path + 'bootstrap-peers.txt'
	all_peers_file = path + 'all-peers.txt'
	good_peers_file = path + 'good-peers.txt'

	test_peers_file = path + 'peers-test.txt'
	bcclient_path = '../'
	'''
	# get boostrap peers
	bootstrap_ips = get_ips_from_dns(get_bootstrap_urls(bootstrap_urls_file))
	write_list_to_file(bootstrap_ips, bootstrap_ips_file)
	
	# get all peers
	ips = get_addresses_from_peers(bootstrap_ips_file, bcclient_path, timeout=300)
	print('Received ' + str(len(ips)) + ' distinct IPs.\n')
	write_list_to_file(ips, all_peers_file)
	
	# get accessible peers
	ips = get_accessible_ips(all_peers_file)
	write_list_to_file(ips, good_peers_file)
	'''

	ips = get_accessible_ips(path + 'good-peers-2018-03-17.txt')
	write_list_to_file(ips, path + 'good-peers-2018-03-19.txt')

if __name__ == "__main__":
    main()