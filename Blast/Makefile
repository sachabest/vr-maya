#-
# ==========================================================================
# Copyright (c) 2011 Autodesk, Inc.
# All rights reserved.
# 
# These coded instructions, statements, and computer programs contain
# unpublished proprietary information written by Autodesk, Inc., and are
# protected by Federal copyright law. They may not be disclosed to third
# parties or copied or duplicated in any form, in whole or in part, without
# the prior written consent of Autodesk, Inc.
# ==========================================================================
#+

ifndef INCL_BUILDRULES

#
# Include platform specific build settings
#
TOP := ..
include $(TOP)/config_16/buildrules


#
# Always build the local plug-in when make is invoked from the
# directory.
#
all : plugins

endif

#
# Variable definitions
#

SRCDIR := $(TOP)/Blast
DSTDIR := $(TOP)/Blast

Blast_SOURCES  := $(TOP)/Blast/blast.cpp
Blast_OBJECTS  := $(TOP)/Blast/blast.o
# Blast_SOURCES  := $(TOP)/Blast/blast.cpp
# Blast_OBJECTS  := $(TOP)/Blast/blast.o
Blast_PLUGIN   := $(DSTDIR)/iBlast.$(EXT)
Blast_MAKEFILE := $(DSTDIR)/Makefile

#
# Include the optional per-plugin Makefile.inc
#
#    The file can contain macro definitions such as:
#       {pluginName}_EXTRA_CFLAGS
#       {pluginName}_EXTRA_C++FLAGS
#       {pluginName}_EXTRA_INCLUDES
#       {pluginName}_EXTRA_LIBS
-include $(SRCDIR)/Makefile.inc


#
# Set target specific flags.
#

$(Blast_OBJECTS): CFLAGS   := $(CFLAGS)   $(Blast_EXTRA_CFLAGS)
$(Blast_OBJECTS): C++FLAGS := $(C++FLAGS) $(Blast_EXTRA_C++FLAGS)
$(Blast_OBJECTS): INCLUDES := $(INCLUDES) $(Blast_EXTRA_INCLUDES)

depend_Blast:     INCLUDES := $(INCLUDES) $(Blast_EXTRA_INCLUDES)

$(Blast_PLUGIN):  LFLAGS   := $(LFLAGS) $(Blast_EXTRA_LFLAGS) 
$(Blast_PLUGIN):  LIBS     := $(LIBS)   -lOpenMaya -lOpenMayaUI -lOpenMayaAnim -lFoundation -framework AGL -framework OpenGL $(Blast_EXTRA_LIBS) 

#
# Rules definitions
#

.PHONY: depend_Blast clean_Blast Clean_Blast


$(Blast_PLUGIN): $(Blast_OBJECTS) 
	-rm -f $@
	$(LD) -o $@ $(LFLAGS) $^ $(LIBS)

depend_Blast :
	makedepend $(INCLUDES) $(MDFLAGS) -f$(DSTDIR)/Makefile $(Blast_SOURCES)

clean_Blast:
	-rm -f $(Blast_OBJECTS)

Clean_Blast:
	-rm -f $(Blast_MAKEFILE).bak $(Blast_OBJECTS) $(Blast_PLUGIN)


plugins: $(Blast_PLUGIN)
depend:	 depend_Blast
clean:	 clean_Blast
Clean:	 Clean_Blast

