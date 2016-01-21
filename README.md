## CIS 099 - Independent Study

### Repository Organization

There are three projects wrapped inside one large Visual Studio 2015 solution.

* Blast: a variation on the Maya blastCmd that outputs the current frame of the currently selected viewport to a specified file. This project is built in VS2015. 

* TransformServer: a variation on the Maya udpDevice MPxThreadedDevice node that is designed to take 3 doubles as input (ideally from the mobile device). These doubles are output variables from the node that can be connected to a camera rotation, for example. 

* FrameServer: a server written in Python/OpenMaya to serve frames from Blast via a UDP server (threaded outside the DG) to a mobile device for display. This command runs completely outside the threads of Blast and can operate on its own by solely reading a file frmo the local filesystem. 

* buildrules: a makefile extension to build using make/cmake/clang on OSX

* buildconfig: another makefile extension to serve the same purpose and buildrules

* Makefile: a top level makefile to build all subdirectories

### Building

The projects included in this repository are intended to be built on either Windows 10 using Visual Studio 2015 or on Mac OS X 10.11 using make. To that end, there are makefiles and vsproj files in each project folder. Output files, however, will vary by platform: Windows will output compiled plugins in .mll format, while Mac will do so in standard *.o and *.bundle files. Importing into Maya should be platform-aware and adaptable to these various output files. 

To build on Windows, simply open the .sln in Visual Studio and click build. Be sure the configuration is set to x64.

To build on Mac, run ``` make ``` on the top level directory to build each subproject. 
