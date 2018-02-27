#!/bin/bash

# Builds the bcclient tool for either mainnet or testnet.

usage="Usage: ./build [mainnet|testnet]"

if [ $# -ne 1 ]; then
	echo $0: $usage
	exit 1
fi

network=$1

if [ "$network"	 = "mainnet" ]; then
	echo "building for" $network "..."
	make clean
	cd libbitcoin
	make clean
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


