#!/bin/bash

# Primitive sanity-check testing

TESTNET_PEER_IP=148.251.191.74
TESTNET_PORT=18333

# Arguments: $1 - test name, $2 - command, $3 - target string in output, $4 target number of matches
run_test() {
	echo -ne $1 ": "
	lines_matched=$($2 | grep "$3" | wc -l)
	if [ -n $4 ]
	then
		if [ $lines_matched -gt 0 ]
		then
			echo "OK"
		else
			echo "Not passed!"
		fi
	else
		if [ $lines_matched -eq $4 ]
		then
			echo "OK"
		else
			echo "Not passed!"
		fi
	fi

}

run_tests() {
	echo "Running tests."
	run_test "Connect to testnet node" "./target/bcclient $TESTNET_PEER_IP -p $TESTNET_PORT" "Verack received." 1
	run_test "Connect to same peer twice" "./target/bcclient $TESTNET_PEER_IP -p $TESTNET_PORT -n 2" "Verack received." 2
	run_test "Connect to 4 peers from peers.txt" "./target/bcclient -f peers.txt" "Verack received." 4
	#run_test "Send getaddr, receive addr" "./target/bcclient $TESTNET_PEER_IP -p $TESTNET_PORT -s getaddr -l addr" "Address message received" 1 # must kill with Ctrl+C
}

run_tests