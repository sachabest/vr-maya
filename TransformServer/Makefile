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

SRCDIR := $(TOP)/transformServer
DSTDIR := $(TOP)/transformServer

transformServer_SOURCES  := $(TOP)/TransformServer/transformServer.cpp
transformServer_OBJECTS  := $(TOP)/TransformServer/transformServer.o
transformServer_PLUGIN   := $(DSTDIR)/transformServer.$(EXT)
transformServer_MAKEFILE := $(DSTDIR)/Makefile

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

$(transformServer_OBJECTS): CFLAGS   := $(CFLAGS)   $(transformServer_EXTRA_CFLAGS)
$(transformServer_OBJECTS): C++FLAGS := $(C++FLAGS) $(transformServer_EXTRA_C++FLAGS)
$(transformServer_OBJECTS): INCLUDES := $(INCLUDES) $(transformServer_EXTRA_INCLUDES)

depend_transformServer:     INCLUDES := $(INCLUDES) $(transformServer_EXTRA_INCLUDES)

$(transformServer_PLUGIN):  LFLAGS   := $(LFLAGS) $(transformServer_EXTRA_LFLAGS) 
$(transformServer_PLUGIN):  LIBS     := $(LIBS)   -lOpenMaya -lOpenMayaUI -lOpenMayaAnim -lFoundation -framework AGL -framework OpenGL $(transformServer_EXTRA_LIBS) 

#
# Rules definitions
#

.PHONY: depend_transformServer clean_transformServer Clean_transformServer


$(transformServer_PLUGIN): $(transformServer_OBJECTS) 
	-rm -f $@
	$(LD) -o $@ $(LFLAGS) $^ $(LIBS)

depend_transformServer :
	makedepend $(INCLUDES) $(MDFLAGS) -f$(DSTDIR)/Makefile $(transformServer_SOURCES)

clean_transformServer:
	-rm -f $(transformServer_OBJECTS)

Clean_transformServer:
	-rm -f $(transformServer_MAKEFILE).bak $(transformServer_OBJECTS) $(transformServer_PLUGIN)


plugins: $(transformServer_PLUGIN)
depend:	 depend_transformServer
clean:	 clean_transformServer
Clean:	 Clean_transformServer

