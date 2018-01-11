#!/bin/bash

# Primitive sanity-check testing: just make and try to connect to one hard-coded testnet peer.

echo "Building..."

# supress STDOUT but not STDERR
if ( make remake > /dev/null ) then
	echo "Build OK"
	if ( ./target/bcclient 148.251.191.74 -p 18333 | grep -q "Version received") then
		echo "Tests OK"
	else
		echo "Tests not passed!"
	fi
fi

