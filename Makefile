#LD_LIBRARY_PATH=/usr/local/lib
CXX 				= g++
CXXFLAGS			= -g -std=c++11

LIBBITCOIN_LIBS		= ./libbitcoin/src/.libs/
LIBBITCOIN_INCLUDES	= ./libbitcoin/include

CFLAGS 				= -I$(LIBBITCOIN_INCLUDES) -I/usr/local/include
LDFLAGS 			= -L$(LIBBITCOIN_LIBS)

BCNAME 				= "bcclient"
GENNAME 			= "generate-addresses"
TAGFILES 			= GPATH GRTAGS GSYMS GTAGS tags

OBJECTS 			= sendutil.o util.o rcvutil.o main.o

SRC 				= ./src/
INCLUDE				= ./include/

all: $(OBJECTS) generate-addresses
	@echo "  CXX $(BCNAME)"
	@$(CXX) $(CXXFLAGS) -Wl,-rpath $(LIBBITCOIN_LIBS)  $(LDFLAGS) -o $(BCNAME) $(OBJECTS)  -lboost_chrono -lboost_system -lbitcoin

tags:
	gtags
	ctags -R .

sendutil.o: $(SRC)sendutil.cpp $(INCLUDE)sendutil.hpp
	@echo "  CXX sendutil.o"
	@$(CXX) $(CXXFLAGS) $(CFLAGS) -c $(SRC)sendutil.cpp

util.o: $(SRC)util.cpp $(INCLUDE)util.hpp
	@echo "  CXX util.o"
	@$(CXX) $(CXXFLAGS) $(CFLAGS) -c $(SRC)util.cpp

rcvutil.o: $(SRC)rcvutil.cpp $(INCLUDE)rcvutil.hpp
	@echo "  CXX rcvutil.o"
	@$(CXX) $(CXXFLAGS) $(CFLAGS) -c $(SRC)rcvutil.cpp

main.o: $(SRC)main.cpp $(INCLUDE)main.hpp
	@echo "  CXX main.o"
	@$(CXX) $(CXXFLAGS) $(CFLAGS) -c $(SRC)main.cpp

generate-addresses: $(SRC)generate-addresses.cpp
	@echo "  CXX $(GENNAME)"
	@$(CXX) $(CXXFLAGS) $(CFLAGS) -o $(GENNAME) $(SRC)generate-addresses.cpp

clean:
	rm -f $(OBJECTS) $(GENNAME) $(BCNAME) $(TAGFILES)

remake: clean all
