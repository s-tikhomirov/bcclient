#!/bin/bash

# Primitive sanity-check testing

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
	run_test "Connect to testnet node" "./target/bcclient 148.251.191.74 -p 18333" "Verack received."
}

run_tests