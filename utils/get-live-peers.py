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

def write_ips_to_file(ips, filename='peers.txt'):
	with open(filename, 'w') as file:
		file.write('# ' + str(int(time.time())) + ' 0\n')
		for ip in ips:
			file.write(ip + '\n')

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


def main():
	path = '/home/sergei/Documents/code/bcclient/bcclient/utils/'
	bootstrap_urls_file = path + 'bootstrap-dns-bitcoin-testnet.txt'
	bootstrap_ips_file = path + 'bootstrap-peers.txt'
	all_peers_file = path + 'peers.txt'
	bcclient_path = '../'

	bootstrap_ips = get_ips_from_dns(get_bootstrap_urls(bootstrap_urls_file))
	write_ips_to_file(bootstrap_ips, bootstrap_ips_file)
	ips = get_addresses_from_peers(bootstrap_ips_file, bcclient_path, timeout=120)
	print('received ' + str(len(ips)) + ' distinct IPs.\n')
	write_ips_to_file(ips, all_peers_file)


if __name__ == "__main__":
    main()