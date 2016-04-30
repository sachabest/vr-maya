//-
// ==========================================================================
// Copyright 2011 Autodesk, Inc. All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk
// license agreement provided at the time of installation or download,
// or which otherwise accompanies this software in either electronic
// or hard copy form.
// ==========================================================================
//+
// Description:
// A simple client device node that uses UDP to transfer data.
// Sample only runs on Linux.
//
// Run Maya and execute the MEL code below.  In a shell,
// run the Python code and enter 3 numbers to update the
// cube's Rotate. 
//
/*
// MEL:
loadPlugin udpDevice;
string $node = `createNode udpDevice`;
string $cube[] = `polyCube`;
connectAttr ($node + ".outputRotate") ($cube[0] + ".Rotate");
setAttr ($node + ".live") 1;
# Python: run from a Linux command line as a Python script
import socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    data = raw_input("Type 3 numbers for Rotate(. to exit): ")
    if data <> '.':
        clientSocket.sendto(data, ("localhost",7555))
    else:
        break
clientSocket.close()
*/

#include "transformServer.h"

// forward declaration

MTypeId transformServer::id(0x00081052);
MObject transformServer::outputRotate;
MObject transformServer::outputRotateX;
MObject transformServer::outputRotateY;
MObject transformServer::outputRotateZ;

transformServer::transformServer() {}

transformServer::~transformServer() {
    destroyMemoryPools();
}

void transformServer::postConstructor() {
    MObjectArray attrArray;
    attrArray.append(transformServer::outputRotate);
    setRefreshOutputAttributes(attrArray);
    // 1024 can be changed to support more or less buffering
    createMemoryPools(1, 1024, sizeof(char));
}

void transformServer::threadHandler(const char* serverName, const char* deviceName) {
    setDone(false);
    if (serverName != NULL && deviceName != NULL)
        printf("udpThreadHandler: %s %s\n",serverName,deviceName);
#ifdef LINUX

    // alloc socket stuff on the stack
    int sock;
    int bytesRead;
    socklen_t addressLength;
    struct sockaddr_in serverAddress, clientAddress;
    
    // linux socket configuration
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(10001);
    serverAddress.sin_addr.s_addr = INADDR_ANY;

    // zero the input
    bzero(&(serverAddress.sin_zero),8);

    // get platform defined max address length
    addressLength = sizeof(struct sockaddr);

    // Error checks
    if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) == -1) {
        // this is how c throws errors
        // go figure
        cout << "Couldn't create socket. Exiting. " << endl;
        return;
    } if (bind(sock,(struct sockaddr *)&serverAddress,
        sizeof(struct sockaddr)) == -1) {
        cout << "Couldn't bind to port. Exiting. " << endl;
        return;
    }

    MStatus status;
    MCharBuffer buffer;
    char receiveBuffer[1024];
    while (!isDone())
    {
        if (!isLive())
            continue;
        
        // select() modifies its parameters so reset everytime
        fd_set read_set;
        FD_ZERO(&read_set);
        FD_SET(sock, &read_set);
        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 500000; // 1/2 second - change to speed up later
        if (select(sock+1, &read_set, NULL, NULL, &tv) == -1) {
            cout << "Socket closed. Exiting. " << endl;
            break;
        }

        if (!FD_ISSET(sock, &read_set)) {
            cout < "No file descriptor. Continuing. " << endl;
            continue;
        }

        receiveBuffer[0] = 0;
        bytesRead = recvfrom(sock,receiveBuffer,1024,0,
            (struct sockaddr *)&clientAddress, &addressLength);
            
        const char *receivedFromServer = inet_ntoa(clientAddress.sin_addr);
        unsigned short receivedFromPort = ntohs(clientAddress.sin_port);
        
        if (receivedFromServer == NULL)
            continue;
        
        printf("(%s , %d) connection : %s \n",receivedFromServer,receivedFromPort, receiveBuffer);

        if (0 != strcmp(serverName, receivedFromServer)) {
            cout << "Server name doesn't match sending server. Continuing. " < endl;
            continue;
        }

        // Get the storage once we have data from the server
        status = acquireDataStorage(buffer);

        // error check
        if (!status)
            continue;

        // scope the thread loop to isolate stack mem
        beginThreadLoop();
        {
            receiveBuffer[bytesRead] = '\0';
            double* doubleData = reinterpret_cast<double*>(buffer.ptr());
            doubleData[0] = 0.0 ; doubleData[1] = 0.0; doubleData[2] = 0.0;
            MStringArray sa;
            MString s(receiveBuffer);
            if (s.split(' ', sa)) {
                if (sa.length() == 3) {
                    for (int i = 0; i < 3; i++) {
                        doubleData[i] = sa[i].isDouble() ? sa[i].asDouble() : 0.0;
                    }
                    cout << doubleData[0] << " " << doubleData[1] << " " << doubleData[2] < endl;
                } else {
                    cout << "Input array wasn't three doubles. Skipping. " < endl;
                }
            }
            pushThreadData(buffer);
        }
        endThreadLoop();
    }
    
    // Close the socket
    close(sock);
#endif // LINUX
    setDone(true);
}

void transformServer::threadShutdownHandler() {
    setDone(true);
}

void* transformServer::creator() {
    return new transformServer;
}

MStatus transformServer::initialize() {
    MStatus status;
    MFnNumericAttribute numAttr;
    outputRotateX = numAttr.create("outputRotateX", "orx", MFnNumericData::kDouble, 0.0, &status);
    MCHECKERROR(status, "create outputRotateX");
    outputRotateY = numAttr.create("outputRotateY", "ory", MFnNumericData::kDouble, 0.0, &status);
    MCHECKERROR(status, "create outputRotateY");
    outputRotateZ = numAttr.create("outputRotateZ", "orz", MFnNumericData::kDouble, 0.0, &status);
    MCHECKERROR(status, "create outputRotateZ");
    outputRotate = numAttr.create("outputRotate", "or", outputRotateX, outputRotateY, 
                                     outputRotateZ, &status);
    MCHECKERROR(status, "create outputRotate");
    
    ADD_ATTRIBUTE(outputRotate);
    ATTRIBUTE_AFFECTS(live, outputRotate);
    ATTRIBUTE_AFFECTS(frameRate, outputRotate);
    ATTRIBUTE_AFFECTS(serverName, outputRotate);
    ATTRIBUTE_AFFECTS(deviceName, outputRotate);
    return MS::kSuccess;
}

MStatus transformServer::compute(const MPlug& plug, MDataBlock& block) {
    MStatus status;
    if (plug == outputRotate || plug == outputRotateX ||
        plug == outputRotateY || plug == outputRotateZ) {
        MCharBuffer buffer;
        if (popThreadData(buffer)) {
            double* doubleData = reinterpret_cast<double*>(buffer.ptr());
            MDataHandle outputRotateHandle = block.outputValue(outputRotate, &status);
            MCHECKERROR(status, "Error in block.outputValue for outputRotate");
            double3& outputRotate = outputRotateHandle.asDouble3();
            outputRotate[0] = doubleData[0];
            outputRotate[1] = doubleData[1];
            outputRotate[2] = doubleData[2];
            block.setClean(plug);
            releaseDataStorage(buffer);
            return (MS::kSuccess);
        }
        else {
            return MS::kFailure;
        }
    }
    return (MS::kUnknownParameter);
}

MStatus initializePlugin(MObject obj) {
    MStatus status;
    MFnPlugin plugin(obj, PLUGIN_COMPANY, "3.0", "Any");
    status = plugin.registerNode("transformServer", 
                                  transformServer::id,
                                  transformServer::creator,
                                  transformServer::initialize,
                                  MPxNode::kClientDeviceNode);
    if (!status) {
        status.perror("failed to registerNode transformServer");
    }
    return status;
}

MStatus uninitializePlugin(MObject obj) {
    MStatus status;
    MFnPlugin plugin(obj);
    status = plugin.deregisterNode(transformServer::id);
    if (!status) {
        status.perror("failed to deregisterNode transformServer");
    }
    return status;
}