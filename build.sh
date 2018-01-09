#!/bin/bash

# Builds the bcclient tool for either mainnet (default) or testnet.

usage="Usage (mainnet is default): ./build [(mainnet)?|testnet]"

if [ $# -gt 1 ]; then
	echo $0: $usage
	exit 1
fi

network=$1

if [ "$network"	 = "mainnet" ]; then
	echo "building for" $network "..."
	sudo apt-get install build-essential autoconf automake libtool libboost-all-dev pkg-config libcurl4-openssl-dev libleveldb-dev shtool
	cd libbitcoin
	ln -s $(which shtool)
	autoreconf -i
	./configure --enable-leveldb
	make
	cd ../
	make
else
	if [ "$network"	 = "testnet" ]; then
		echo "building for" $network "..."
		make clean
		cd libbitcoin
		make clean
		./configure --enable-leveldb --enable-testnet
		make
		cd ../
		make
	else
		echo $0: $usage
	fi
fi


