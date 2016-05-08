#define LINUX
#ifdef LINUX // change to OSX l8r
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#endif

#include <maya/MFnPlugin.h>
#include <maya/MTypeId.h>
#include <api_macros.h>
#include <maya/MIOStream.h>
#include <maya/MString.h>
#include <maya/MStringArray.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MPxClientDeviceNode.h>

using namespace std;

class transformServer : public MPxClientDeviceNode {
public:
    transformServer();
    virtual         ~transformServer();
    
    virtual void        postConstructor();
    virtual MStatus     compute( const MPlug& plug, MDataBlock& data );
    virtual void        threadHandler( const char* serverName, const char* deviceName );
    virtual void        threadShutdownHandler();
    static void*        creator();
    static MStatus      initialize();

    static MObject      outputRotate;
    static MObject      outputRotateX;
    static MObject      outputRotateY;
    static MObject      outputRotateZ;

    static MTypeId      id;
private:

};