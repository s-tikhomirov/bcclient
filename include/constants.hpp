#ifndef CONSTANTS_HPP
#define CONSTANTS_HPP

#include <cstdint>

constexpr uint16_t BITCOIN_MAINNET_PORT = 8333;
constexpr uint16_t BITCOIN_TESTNET_PORT = 18333;
constexpr uint16_t ZCASH_MAINNET_PORT = 8233;
constexpr uint16_t ZCASH_TESTNET_PORT = 18233;

constexpr uint16_t CHOSEN_PORT = ZCASH_MAINNET_PORT;

constexpr uint16_t THREADS = 1;	// was 4

#endif