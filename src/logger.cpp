/* Copyright (c) 2018 Sergei Tikhomirov
 Distributed under the MIT/X11 software license, see the accompanying
 file LICENSE or http://www.opensource.org/licenses/mit-license.php. */

#include <bitcoin/bitcoin.hpp>
#include "../include/logger.hpp"
#include "../include/util.hpp"

using std::placeholders::_1;
using std::placeholders::_2;
using std::placeholders::_3;

Logger::Logger(const std::string& logFilename, bool fPrintDebug) {
  log_info() << "Initializing logging to file.";
  std::ofstream logfile;
  if(!logFilename.empty())
  {
    logfile.open(logFilename, std::ios_base::app);
    log_info().set_output_function(std::bind(output_to_file, std::ref(logfile), _1, _2, _3));
    log_debug().set_output_function(std::bind(output_to_file, std::ref(logfile), _1, _2, _3));
    log_error().set_output_function(std::bind(output_to_file, std::ref(logfile), _1, _2, _3));
  } else {
    log_info() << "Initializing logging to colsole.";
    log_info().set_output_function(output_to_terminal);
    log_debug().set_output_function(output_to_terminal);
    log_error().set_output_function(output_to_terminal);
  }  
  if (!fPrintDebug) {
    log_debug().set_output_function(std::bind(output_to_null, std::ref(logfile), _1, _2, _3));
  }
}  
