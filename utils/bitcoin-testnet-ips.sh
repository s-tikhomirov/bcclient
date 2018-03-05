#!/bin/bash
# Source: https://bitcoin.stackexchange.com/a/48734/31712

for i in testnet-seed.bitcoin.jonasschnelli.ch \
    seed.tbtc.petertodd.org \
    testnet-seed.bluematt.me \
    testnet-seed.bitcoin.schildbach.de
do
    nslookup $i 2>&1 | grep Address | cut -d' ' -f2
done
