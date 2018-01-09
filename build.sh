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

