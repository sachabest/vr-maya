// Referenced from iBlastCmd.cpp (Copyright 2015 Autodesk)

#include "blast.h"

#pragma mark GLBuffer

MyMPxGlBuffer::MyMPxGlBuffer(M3dView &view) : MPxGlBuffer(view) {}

MyMPxGlBuffer::~MyMPxGlBuffer() {}

void MyMPxGlBuffer::beginBufferNotify() {
	glClearColor(0.0, 0.0, 0.0, 0.0);
}

void MyMPxGlBuffer::endBufferNotify() {}

#pragma mark Creation and Destruction

iBlastCmd::iBlastCmd() {
	offBuff = NULL;
}

iBlastCmd::~iBlastCmd() {
	delete offBuff;
}

void *iBlastCmd::creator() {
	return (void *)(new iBlastCmd);
}

#pragma mark Argument Handling

MSyntax iBlastCmd::newSyntax() {
	MSyntax syntax;
	syntax.addFlag(kOnscreenFlag, kOnscreenFlagLong);
	syntax.addFlag(kFilenameFlag, kFilenameFlagLong, MSyntax::kString);
	syntax.addFlag(kPanelFlag, kPanelFlagLong, MSyntax::kString);
	return syntax;
}

MStatus iBlastCmd::parseArgs(const MArgList& args) {
	MStatus stat = MS::kSuccess;
	MArgDatabase argData(syntax(), args);
	onscreen = argData.isFlagSet(kOnscreenFlag);
	start = 0.0;
	if (argData.isFlagSet(kFilenameFlag)) {
		stat = argData.getFlagArgument(kFilenameFlag, 0, filename);
	} else {
		filename = "blastOut";
	}
	if (argData.isFlagSet(kPanelFlag)) {
		argData.getFlagArgument(kPanelFlag, 0, panel);
	} else {
		panel = "modelPanel1";
	}
	return stat;
}

MStatus iBlastCmd::fileDump(MTime frame) {
	MStatus stat = MS::kFailure;

	char msgBuffer[256]; // to save xostly stdout calls

	MImage iffOutput;
	if (iffOutput.create(fWidth, fHeight) != MS::kSuccess) {
		cerr << "Failed to create output image\n" << endl;
		return MS::kFailure;
	}

	unsigned char *iffPixels = iffOutput.pixels();
	unsigned char *glPixels = fPixels;

	for (int pixCtr = 0; pixCtr < fPixelCnt; pixCtr++) {
		*iffPixels = *glPixels;     // R
		glPixels++;
		iffPixels++;
		*iffPixels = *glPixels;     // G 
		glPixels++;
		iffPixels++;
		*iffPixels = *glPixels;     // B
		glPixels++;
		iffPixels++;
		*iffPixels = *glPixels;     // A
		glPixels++;
		iffPixels++;
	};

	if (iffOutput.writeToFile(filename, "png") != MS::kSuccess) {
		sprintf(msgBuffer, "Failed to output image to %s\n", filename.asChar());
		MGlobal::displayError(msgBuffer);
		stat = MS::kFailure;
	} else {
		// sprintf(msgBuffer, "output from %s buffer to %s done.\n",
		// 	(onscreen ? "on-screen" : "off-screen"),
		// 	filename.asChar());
		// MGlobal::displayInfo(msgBuffer);
		stat = MS::kSuccess;
	}

	return stat;
}

MStatus iBlastCmd::doIt(const MArgList& args) {
	char msgBuffer[256];
	MStatus stat = MS::kFailure;
	stat = parseArgs(args);
	if (!stat) {
		sprintf(msgBuffer, "Failed to parse args for %s command\n", commandName);
		MGlobal::displayError(msgBuffer);
		return stat;
	}

	// change this to support oculus 2 views at once?
	M3dView view;
	stat = M3dView::getM3dViewFromModelPanel(panel, view);
	if ( !stat ) {
		sprintf( msgBuffer, "Failed to get view for %s command\n", commandName );
		MGlobal::displayError( msgBuffer );
		return stat;
	}

	// this can change - see resizing M3dView
	fWidth = (short)view.portWidth();
	fHeight = (short)view.portHeight();
	fPixelCnt = fWidth * fHeight;

	// allocate
	fPixels = new uchar_t[fPixelCnt * 4];

	// check allocation
	if (!fPixels) {
		MGlobal::displayError("Failed to allocate memory for reading pixels\n");
		return MS::kFailure;
	}

	if (!onscreen) {
		offBuff = new MyMPxGlBuffer(view);
		if (!offBuff->openFbo(fWidth, fHeight, view))
		{
			MGlobal::displayError("Failed to open offscreen buffer\n");
			delete offBuff;
			offBuff = NULL;
			return MS::kFailure;
		}
	}

	MAnimControl::setCurrentTime(start);
	if (!onscreen) {
		//  Refresh the view to the off-screen buffer.  The arguments
		//  "all" and "force" to the normal refresh call are
		//  unnecessary because the refresh is always forced and is
		//  never to more than this single view.
		view.refresh(*offBuff, true);
		offBuff->bindFbo();
	} else {
		// We are not using an off-screen buffer.  Simply refresh
		// the on-screen window.
		view.refresh(false /* all */, true /* force */);
		glReadBuffer(GL_FRONT);
	}

	view.beginGL();
	glPixelStorei(GL_PACK_ALIGNMENT, 1);
	glReadPixels(0, 0, fWidth, fHeight, GL_RGBA, GL_UNSIGNED_BYTE, fPixels);
	view.endGL();

	if (offBuff) {
		offBuff->unbindFbo();
	}

	// Output the pixels to disk    
	fileDump(start);

	// deallocate

	if (offBuff) {
		offBuff->closeFbo(view);
		delete offBuff;
		offBuff = NULL;
	}

	delete[] fPixels;
	return stat;
}

#pragma mark Plugin Initialization

MStatus initializePlugin(MObject obj) {
	MStatus status;
	MFnPlugin plugin(obj, CREATOR, "6.0", "Any");
	status = plugin.registerCommand(commandName,
		iBlastCmd::creator,
		iBlastCmd::newSyntax);
	if (!status) {
		status.perror("registerCommand");
		return status;
	}
	return status;
}

MStatus uninitializePlugin(MObject obj) {
	MStatus status;
	MFnPlugin plugin(obj);
	status = plugin.deregisterCommand(commandName);
	if (!status) {
		status.perror("deregisterCommand");
		return status;
	}
	return status;
}