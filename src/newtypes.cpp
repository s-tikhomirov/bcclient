/* Copyright (c) 2018 Sergei Tikhomirov
 Distributed under the MIT/X11 software license, see the accompanying
 file LICENSE or http://www.opensource.org/licenses/mit-license.php. */

#include "../include/newtypes.hpp"

#include <iostream>
#include <vector>
#include <map>

Address::Address(std::string ip_, uint16_t port_) : ip(ip_), port(port_) {}

std::string Address::toString() const {
	return ip + ":" + std::to_string(port);
}	


Connection::Connection(Address address_, ConnectionType connectionType_, uint16_t connectionId_, ConnectionState connectionState_) 
	: address(address_), 
	connectionType(connectionType_),
	connectionId(connectionId_),
	connectionState(connectionState_),
	pong_remained(0),
	pong_waittime(0),
	fGetAddrSentConfirmed(false),
	numGetAddrToSend(0),
	addr_timeoffset(0)
	{ }

std::string Connection::toString() const {
	return address.toString() + "." + std::to_string(connectionId);
}

BlockchainProber::BlockchainProber(
	const std::string& peersFilename_,
	const std::string& blocksFilename_,
	uint16_t port_,
	uint16_t listenPort_)
	:
	peersFilename(peersFilename_),
	blocksFilename(blocksFilename_),
	port(port_),
	listenPort(listenPort_)
	{ }

std::string BlockchainProber::toString() const {
	return "Blockchain prober: port=" + std::to_string(port) + 
	", listenPort=" + std::to_string(listenPort);
}


/*
int main() {
	std::cout << "in peersmap.cpp" << std::endl;
	
	return 0;
}
*/
