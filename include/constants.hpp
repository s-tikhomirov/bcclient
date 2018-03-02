#ifndef CONSTANTS_HPP
#define CONSTANTS_HPP

#include <map>
#include <cstdint>
#include <bitcoin/constants.hpp>
#include <bitcoin/primitives.hpp>

using namespace libbitcoin;

constexpr uint16_t THREADS = 1;	// was 4

// Despite the name, it's Recipient Address,  
// see ./include/bitcoin/satoshi_serialize.hpp +48 for serialization.
const ip_address_type address_me_bitcoin = 
	ip_address_type{0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0xff, 0xff, 0xd8, 0x96, 0x9b, 0x97};

// It's Sender Address
const ip_address_type address_you_bitcoin = 
	ip_address_type{0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0xff, 0xff, 0xd8, 0x96, 0x9b, 0x98};

const ip_address_type address_me_zcash = 
	ip_address_type{0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0xff, 0xff, 0x68, 0xec, 0xb4, 0xe7};

const ip_address_type address_you_zcash = 
	ip_address_type{0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0xff, 0xff, 0x5a, 0xf7, 0xbd, 0x26};

const std::map<uint32_t, uint16_t> PORT = {
	{0xd9b4bef9, 8333},		// Bitcoin mainnet
	{0x0709110b, 18333},	// Bitcoin testnet
	{0x6427e924, 8233},		// Zcash mainnet
	{0xbff91afa, 18233}		// Zcash testnet
};

const std::map<uint32_t, uint32_t> VERSION = {
	{0xd9b4bef9, 70014},		// Bitcoin mainnet
	{0x0709110b, 70014},		// Bitcoin testnet
	{0x6427e924, 170003},		// Zcash mainnet
	{0xbff91afa, 170003}		// Zcash testnet
};

const std::map<uint32_t, uint32_t> SERVICES = {
	{0xd9b4bef9, 7},		// Bitcoin mainnet
	{0x0709110b, 7},		// Bitcoin testnet
	{0x6427e924, 1},		// Zcash mainnet
	{0xbff91afa, 1}			// Zcash testnet
};

const std::map<uint32_t, ip_address_type> ADDRESS_ME = {
	{0xd9b4bef9, address_me_bitcoin},		// Bitcoin mainnet
	{0x0709110b, address_me_bitcoin},		// Bitcoin testnet
	{0x6427e924, address_me_zcash},			// Zcash mainnet
	{0xbff91afa, address_me_zcash}			// Zcash testnet
};

const std::map<uint32_t, ip_address_type> ADDRESS_YOU = {
	{0xd9b4bef9, address_you_bitcoin},		// Bitcoin mainnet
	{0x0709110b, address_you_bitcoin},		// Bitcoin testnet
	{0x6427e924, address_you_zcash},		// Zcash mainnet
	{0xbff91afa, address_you_zcash}			// Zcash testnet
};

// Latest update: 2018-03-02
const std::map<uint32_t, uint32_t> RECENT_HEIGHT = {
	{0xd9b4bef9, 511650},		// Bitcoin mainnet
	{0x0709110b, 1287119},		// Bitcoin testnet
	{0x6427e924, 281366},		// Zcash mainnet
	{0xbff91afa, 197598}		// Zcash testnet
};

#endif