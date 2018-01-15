#!/bin/bash

# Primitive sanity-check testing

TESTNET_PEER_IP=148.251.191.74
TESTNET_PORT=18333

run_test() {
	echo -ne $1 ": "
	if ( $2 | grep -q "$3" ) then
		echo "OK"
	else
		echo "Not passed!"
	fi
}

run_tests() {
	echo "Running tests."
	run_test "Connect to testnet node" "./target/bcclient $TESTNET_PEER_IP -p $TESTNET_PORT" "Verack received."
	run_test "Connect to 4 peers from peers.txt" "./target/bcclient -f peers.txt" "Added 4 addresses"
	run_test "Send getaddr, receive addr" "./target/bcclient $TESTNET_PEER_IP -p $TESTNET_PORT -s getaddr -l addr" "Address message received" # must kill with Ctrl+C
}

run_tests