/* Copyright (c) 2018 Sergei Tikhomirov
 Distributed under the MIT/X11 software license, see the accompanying
 file LICENSE or http://www.opensource.org/licenses/mit-license.php. */

#ifndef LOGGER_H
#define LOGGER_H

#include <iostream>

using namespace bc;

class Logger {
  std::ofstream logStream;
public:
  Logger(char *logFilename, bool fPrintDebug);
};

#endif