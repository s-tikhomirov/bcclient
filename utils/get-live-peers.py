#! /usr/bin/python3

import subprocess
import socket
import time, datetime
import re
from multiprocessing import Pool
import itertools

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

def get_addresses_from_peers(peers_filename, bcclient_path='../', timeout=240):
	print("Receiving addr from peers in " + peers_filename + "...")
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
	print('Received ' + str(len(ips)) + ' distinct IPs.\n')
	return ips

def is_live(response):
	return (('Version received' in response) and ('Verack received' in response))

def get_live_ips(ips, bcclient_path='../', timeout=1):
	good_ips = []
	bad_ips = []
	total_ips = len(ips)
	print("Total " + str(total_ips) + " IPs in file.")
	counter = 0
	for ip in ips:
		if (counter % 10 == 0):
			print("Checking IP " + str(counter) + " of " + str(total_ips))
		response = ''
		try:
			response = subprocess.check_output('timeout ' + str(timeout) + ' ./bcclient ' + ip, 
				shell=True,
				cwd=bcclient_path).decode('utf-8')
		except subprocess.CalledProcessError:
			pass	# ignore exit on timeout: peer is inaccessible
		if is_live(response):
			good_ips.append(ip)
		else:
			bad_ips.append(ip)
		counter += 1
	print(str(len(good_ips)) + ' accessible, ' + str(len(bad_ips)) + ' inaccessible IPs.')
	return good_ips

def get_live_ips_parallel(ips, n=32):
	print("Checking liveness in " + str(n) + " threads...")
	pool = Pool(processes=n)
	ips_chunks = [ips[i::n] for i in range(n)]
	print("Divided " + str(len(ips)) + " into " + str(len(ips_chunks)) + " chunks.")
	live_ips = [pool.apply_async(get_live_ips, (ips_chunks[i], )) for i in range(n)]
	print("Total: " + str(len(live_ips)) + " live peers.")
	return [item for sublist in [res.get() for res in live_ips] for item in sublist]


def main():
	path = '/home/sergei/Documents/code/bcclient/bcclient/utils/'
	bootstrap_filename = path + 'bootstrap-dns-bitcoin-testnet.txt'
	bootstrap_ips_file = path + 'bootstrap-peers_' + str(datetime.datetime.now().date()) +'.txt'
	live_ips_file = path + 'live-peers_' + str(datetime.datetime.now().date()) +'.txt'
	
	# get boostrap peers
	bootstrap_ips = get_ips_from_dns(get_bootstrap_urls(bootstrap_filename))
	write_list_to_file(bootstrap_ips, bootstrap_ips_file)
	
	# get addr from bootstrap peers
	all_ips_1 = get_addresses_from_peers(bootstrap_ips_file)

	# filter live peers (round 1)
	ips_live_1 = get_live_ips_parallel(all_ips_1)
	write_list_to_file(ips_live_1, path + 'live-peers_1_' + str(datetime.datetime.now().date()) +'.txt')
	
	# get addr from all live peers
	all_ips_2 = get_addresses_from_peers(path + 'live-peers_1_' + str(datetime.datetime.now().date()) +'.txt')

	# filter live peers (round 2)
	ips_live_2 = get_live_ips_parallel([ip for ip in all_ips_2 if ip not in all_ips_1])
	write_list_to_file(ips_live_2, path + 'live-peers_2_' + str(datetime.datetime.now().date()) +'.txt')

	write_list_to_file(ips_live_1 + ips_live_2, live_ips_file)


if __name__ == "__main__":
    main()