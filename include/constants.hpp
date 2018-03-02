#ifndef CONSTANTS_HPP
#define CONSTANTS_HPP

#include <map>
#include <cstdint>
#include <bitcoin/constants.hpp>
#include <bitcoin/primitives.hpp>

constexpr uint16_t THREADS = 1;	// was 4

const std::map<uint32_t, uint16_t> PORTS = {
	{0xd9b4bef9, 8333},
	{0x0709110b, 18333},
	{0x6427e924, 8233},
	{0xbff91afa, 18233}
};

#endif