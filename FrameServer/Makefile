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
include $(TOP)/buildrules


#
# Always build the local plug-in when make is invoked from the
# directory.
#
all : plugins

endif

#
# Variable definitions
#

SRCDIR := $(TOP)/FrameServer
DSTDIR := $(TOP)/FrameServer

FrameServer_SOURCES  := $(TOP)/FrameServer/frameServer.cpp
FrameServer_OBJECTS  := $(TOP)/FrameServer/frameServer.o
FrameServer_PLUGIN   := $(DSTDIR)/frameServer.$(EXT)
FrameServer_MAKEFILE := $(DSTDIR)/Makefile

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

$(FrameServer_OBJECTS): CFLAGS   := $(CFLAGS)   $(FrameServer_EXTRA_CFLAGS)
$(FrameServer_OBJECTS): C++FLAGS := $(C++FLAGS) $(FrameServer_EXTRA_C++FLAGS)
$(FrameServer_OBJECTS): INCLUDES := $(INCLUDES) $(FrameServer_EXTRA_INCLUDES)

depend_FrameServer:     INCLUDES := $(INCLUDES) $(FrameServer_EXTRA_INCLUDES)

$(FrameServer_PLUGIN):  LFLAGS   := $(LFLAGS) $(FrameServer_EXTRA_LFLAGS) 
$(FrameServer_PLUGIN):  LIBS     := $(LIBS)   -lOpenMaya -lOpenMayaUI -lOpenMayaAnim -lFoundation -framework AGL -framework OpenGL $(FrameServer_EXTRA_LIBS) 

#
# Rules definitions
#

.PHONY: depend_FrameServer clean_FrameServer Clean_FrameServer


$(FrameServer_PLUGIN): $(FrameServer_OBJECTS) 
	-rm -f $@
	$(LD) -o $@ $(LFLAGS) $^ $(LIBS)

depend_FrameServer :
	makedepend $(INCLUDES) $(MDFLAGS) -f$(DSTDIR)/Makefile $(FrameServer_SOURCES)

clean_FrameServer:
	-rm -f $(FrameServer_OBJECTS)

Clean_FrameServer:
	-rm -f $(FrameServer_MAKEFILE).bak $(FrameServer_OBJECTS) $(FrameServer_PLUGIN)


plugins: $(FrameServer_PLUGIN)
depend:	 depend_FrameServer
clean:	 clean_FrameServer
Clean:	 Clean_FrameServer

