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


/*
int main() {
	std::cout << "in peersmap.cpp" << std::endl;
	Address a = Address { "127.0.0.1", 18333 };
	Connection c = Connection(a);
	std::cout << c.toString() << std::endl;
	return 0;
}
*/
