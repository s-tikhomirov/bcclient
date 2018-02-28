#ifndef CONSTANTS_HPP
#define CONSTANTS_HPP

#include <cstdint>
#include <bitcoin/constants.hpp>
#include <bitcoin/primitives.hpp>

constexpr uint16_t DEFAULT_PORT = libbitcoin::protocol_port;

constexpr uint16_t THREADS = 1;	// was 4

enum Network {
  BITCOIN_MAINNET,
  BITCOIN_TESTNET,
  ZCASH_MAINNET,
  ZCASH_TESTNET
};

// Don't forget to change:
// * magic numbers in libbitcoin/src/constants.cpp
// * port numbers in libbitcoin/include/bitcoin/constants.hpp
constexpr Network NETWORK = Network::ZCASH_TESTNET;

#endif