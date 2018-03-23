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
	print("Getting IPs from bootstrap DNS entries...")
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
	print("Receiving addr from peers in " + peers_filename + " (wait " + str(timeout) + " seconds)...")
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
	#print("Total " + str(total_ips) + " IPs in file.")
	counter = 0
	for ip in ips:
		#if (counter % 10 == 0):
		#	print("Checking IP " + str(counter) + " of " + str(total_ips))
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
	#print(str(len(good_ips)) + ' accessible, ' + str(len(bad_ips)) + ' inaccessible IPs.')
	return good_ips

def get_live_ips_parallel(ips, n=32):
	print("Checking liveness in " + str(n) + " threads...")
	pool = Pool(processes=n)
	ips_chunks = [ips[i::n] for i in range(n)]
	#print("Divided " + str(len(ips)) + " into " + str(len(ips_chunks)) + " chunks.")
	live_ips = [pool.apply_async(get_live_ips, (ips_chunks[i], )) for i in range(n)]
	return [item for sublist in [res.get() for res in live_ips] for item in sublist]

# take a list of (presumably live) IPs
# for all IPs in list, go getaddr-addr
# check all received addresses for liveness, return the list of live peers
def round(live_ips, path_to_tmp_files):
	peers_tmp_filename = path_to_tmp_files + 'peers_' + str(int(time.time())) + '.txt'
	write_list_to_file(live_ips, peers_tmp_filename)	# temporary file; will be overwritten
	new_all_ips = get_addresses_from_peers(peers_tmp_filename, timeout=600)
	new_live_ips = get_live_ips_parallel([ip for ip in new_all_ips if ip not in live_ips])
	print("Detected " + str(len(new_live_ips)) + " new live peers.")
	return live_ips + new_live_ips

def rounds(ips, num_rounds, path_to_tmp_files):
	live_ips = ips
	print("We know of " + str(len(live_ips)) + " live peers.")
	for n in range(num_rounds):
		write_list_to_file(live_ips, filename='peers-' + str(datetime.datetime.now().date()) + '.txt')
		print(datetime.datetime.now())
		print("\nRound " + str(n) + ":")
		live_ips = round(live_ips, path_to_tmp_files)
		print("We know of " + str(len(live_ips)) + " live peers.")
	return live_ips

def main():
	network = 'bitcoin-testnet'
	path = '/home/sergei/Documents/code/bcclient/bcclient/utils/'
	bootstrap_dns_filename = path + 'bootstrap-dns-' + network + '.txt'
	bootstrap_ips_file = path + 'bootstrap-peers-' + network + '_' + str(datetime.datetime.now().date()) +'.txt'

	bitcoind_ips = [] # optionally, add some peers that ur full node connected to

	print(datetime.datetime.now())
	bootstrap_ips = get_live_ips_parallel(get_ips_from_dns(get_bootstrap_urls(bootstrap_dns_filename)))
	initial_ips = list(set(bitcoind_ips + bootstrap_ips))
	live_ips = rounds(initial_ips, 3, path_to_tmp_files=path)
	write_list_to_file(live_ips, filename='peers-' + network + "_" + str(datetime.datetime.now().date()) + '.txt')


if __name__ == "__main__":
    main()