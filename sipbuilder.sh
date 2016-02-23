#!/usr/bin/env bash
MAYAPYQTBUILD="`dirname \"$0\"`" # Relative
export MAYAPYQTBUILD="`( cd \"$MAYAPYQTBUILD\" && pwd )`" #
Absolutized and
normalized
cd $MAYAPYQTBUILD
export SIPDIR=$MAYAPYQTBUILD/sip-4.16.7
export MAYA_LOCATION=/Applications/Autodesk/maya2016
cd $SIPDIR
$MAYA_LOCATION/Maya.app/Contents/bin/mayapy ./configure.py --
arch=x86_64
make
sudo make install