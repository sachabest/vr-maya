#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <maya/MFStream.h>
#include <maya/M3dView.h>
#include <maya/MPxGlBuffer.h>
#include <maya/MFnPlugin.h>
#include <maya/MString.h>
#include <maya/MArgList.h>
#include <maya/MPxCommand.h>
#include <maya/MSyntax.h>
#include <maya/MArgDatabase.h>
#include <maya/MGlobal.h>
#include <maya/MAnimControl.h>
#include <maya/MImage.h>
#include <maya/MIOStream.h>

// Use this to choose between Linux MIFF files and Maya's standard IFF format for output
#define OUTPUT_IFF_FILES
typedef unsigned char uchar_t;
#define kOnscreenFlag       "-o"
#define kOnscreenFlagLong   "-onscreen"
#define kFilenameFlag       "-f"
#define kFilenameFlagLong   "-filename"
#define kStartFlag          "-s"
#define kStartFlagLong      "-start"
#define kEndFlag            "-e"
#define kEndFlagLong        "-stop"
#define commandName         "blast"
// Offscreen buffer
class MyMPxGlBuffer : public MPxGlBuffer {
public:
	MyMPxGlBuffer(M3dView &view);
	virtual ~MyMPxGlBuffer();

	virtual void beginBufferNotify();
	virtual void endBufferNotify();
};

//
// Command class declaration
//
class blastCmd : public MPxCommand
{
public:
	blastCmd();
	virtual         ~blastCmd();
	MStatus         doIt(const MArgList& args);
	static MSyntax  newSyntax();
	static void*    creator();
private:
	MStatus         fileDump(MTime);
	MStatus         parseArgs(const MArgList& args);
	bool            onscreen;
	MString         filename;
	MTime           start;
	MTime           end;
	MyMPxGlBuffer   *offBuff;
	short           fHeight;
	short           fWidth;
	int             fPixelCnt;
	uchar_t         *fPixels;
};