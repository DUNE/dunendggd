CXX = g++
ROOTCONFIG := $(shell which root-config)
ROOTCFLAGS := $(shell $(ROOTCONFIG) --cflags)
ROOTLIBS := $(shell $(ROOTCONFIG) --libs)
EDEP_LIBS = -L $(EDEPSIM_LIB) -ledepsim_io  $(CLHEP_LIBS)
EDEP_INC = -I$(EDEPSIM_INC) -I$(GEANT4_INC) -I$(CLHEP_INC) -ledepsim_io
CXXFLAGS := -g -Wall -Wextra -DNDEBUG -O0 -I $(DUNE_PLOT_STYLE_INC)

SRCS = $(wildcard *.cpp)
OBJS = $(SRCS:.cpp=.o)
EXEC = $(SRCS:.cpp=)

BRANCH_NAME := $(shell git rev-parse --abbrev-ref HEAD)
GIT_STATUS := $(shell git diff-index --quiet HEAD -- src/ app/ || echo "-modified")

CXXFLAGS += -DGIT_BRANCH_NAME=\"$(BRANCH_NAME)$(GIT_STATUS)\"

.PHONY: all clean

all: $(EXEC)

#$(EXEC): $(OBJS)
#$(EXEC): %: %.o 
$(EXEC): %: %.o
	$(CXX) $*.o -o $@ $(ROOTLIBS) $(EDEP_LIBS)

%.o: %.cpp
	$(CXX) $(ROOTCFLAGS) $(CXXFLAGS) $(EDEP_INC) -c $< -o $@
	
# Generate dependency files
%.d: %.cpp
	$(CXX) $(ROOTCFLAGS) $(CXXFLAGS) $(EDEP_INC) -MM -MP -MF $@ $<

# Include dependency files
-include $(SRCS:.cpp=.d)

clean:
	rm -f $(OBJS) $(EXEC)
