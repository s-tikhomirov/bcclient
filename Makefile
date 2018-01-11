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

SRC_DIR 			= ./src/
INCLUDE_DIR			= ./include/
TARGET_DIR			= ./target/

all: $(OBJECTS) generate-addresses
	@echo " CXX $(BCNAME)"
	@$(CXX) $(CXXFLAGS) -Wl,-rpath $(LIBBITCOIN_LIBS)  $(LDFLAGS) -o $(TARGET_DIR)$(BCNAME) $(OBJECTS)  -lboost_chrono -lboost_system -lbitcoin

tags:
	gtags
	ctags -R .

%.o: $(SRC_DIR)%.cpp $(INCLUDE_DIR)%.hpp
	@echo " CXX" $<
	@$(CXX) $(CXXFLAGS) $(CFLAGS) -c $<

generate-addresses: $(SRC_DIR)generate-addresses.cpp
	@echo " CXX" $<
	@$(CXX) $(CXXFLAGS) $(CFLAGS) -o $(GENNAME) $<

clean:
	rm -f $(OBJECTS) $(GENNAME) $(BCNAME) $(TAGFILES)

remake: clean all
