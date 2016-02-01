#include <iostream>

#include "frameServer.h"

DeclareSimpleCommand(HelloWorld, "Autodesk", "2016");

MStatus HelloWorld::doIt(const MArgList&)
{
	std::cout << "Hello World\n" << std::endl;
	return MS::kSuccess;
}