/* Copyright (c) 2018 Sergei Tikhomirov
 Distributed under the MIT/X11 software license, see the accompanying
 file LICENSE or http://www.opensource.org/licenses/mit-license.php. */

#ifndef PEERSMAP_H
#define PEERSMAP_H

#include <iostream>
#include <vector>
#include <map>

enum ConnectionState {
  CONNECTING,
  CONNECTED,
  DISCONNECTED
};

enum PeerState {
	ALIVE,
	DEAD
};

enum ConnectionType {
	INBOUND,
	OUTBOUND
};

class Address {
	std::string ip;
	uint16_t port;
public:
	Address(std::string ip_, uint16_t port_);
	std::string toString() const;
};

class Connection {
	const Address address;
	const ConnectionType connectionType;
	const uint16_t connectionId;
	
	ConnectionState connectionState; // Keep connection state to decide when to reconnect

public:

	int pong_remained; 	// How many pong messages we need to wait for.
	int pong_waittime;	// Until which we should wait for a 'pong' messages. This relies on that we receive other
						// 'raw' messages. Once we receive a non-pong raw message, we check if pong_waittime has come;
						// if yes we descrease pong_remained by one.

	bool fGetAddrSentConfirmed; // false if we are still waiting a successful sent notification of 'getaddr' message
	int numGetAddrToSend; // Number of getaddr messages we need to send
	int addr_timeoffset; // Offset for addresses which we send as a payload in 'addr' messages


	Connection(Address address_, ConnectionType connectionType_ = OUTBOUND, uint16_t connectionId_ = 0, ConnectionState connectionState_ = DISCONNECTED);
	std::string toString() const;

};


#endif