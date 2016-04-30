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

// for GL pixels
typedef unsigned char uchar_t;

#define kOnscreenFlag       "-o"
#define kOnscreenFlagLong   "-onscreen"
#define kFilenameFlag       "-f"
#define kFilenameFlagLong   "-filename"
#define kPanelFlag 			"-p"
#define kPanelFlagLong		"-panel"
#define commandName         "iBlast"
#define CREATOR 			"Sacha Best"

#pragma mark GLBuffer Definition

class MyMPxGlBuffer : public MPxGlBuffer {
public:
	MyMPxGlBuffer(M3dView &view);
	virtual ~MyMPxGlBuffer();

	virtual void beginBufferNotify();
	virtual void endBufferNotify();
};

#pragma mark Command Definition

class iBlastCmd : public MPxCommand {
public:
	iBlastCmd();
	virtual         ~iBlastCmd();
	MStatus         doIt(const MArgList& args);
	static MSyntax  newSyntax();
	static void     *creator();
private:
	MStatus         fileDump(MTime);
	MStatus         parseArgs(const MArgList& args);
	bool            onscreen;
	MString         filename;
	MString 		panel;
	MTime           start;
	MyMPxGlBuffer   *offBuff;
	short           fHeight;
	short           fWidth;
	int             fPixelCnt;
	uchar_t         *fPixels;
};