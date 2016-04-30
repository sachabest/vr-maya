//
//  TransformServer.m
//  maya-client.ios
//
//  Created by Sacha Best on 4/28/16.
//  Copyright © 2016 Sacha Best. All rights reserved.
//

#import "TransformServer.h"

@implementation TransformServer

static TransformServer *instance;

+ (TransformServer *)instance {
    if (!instance) {
        instance = [[TransformServer alloc] init];
        [instance create];
    }
    return instance;
}

- (void)create {
    if (socket || thread) {
        [NSException raise:@"Cannot create socket" format:@"A socket is already open. Please close it before opening a new one. "];
    } else {
        thread = dispatch_queue_create("com.sachabest.maya-client-ios.TransformServer", 0);
        socket = [[GCDAsyncUdpSocket alloc] initWithDelegate:instance delegateQueue:thread];
        gyroManager = [[CMMotionManager alloc] init];
        gyroQueue = [[NSOperationQueue alloc] init];

    }
}

- (void)disconnect {
    if (!socket || !thread) {
        return; // nothing to do
    } else {
        dispatch_suspend(thread);
        socket = NULL;
        thread = NULL;
    }
}
    
- (void)startSendingData {
    [gyroManager startDeviceMotionUpdatesToQueue:gyroQueue withHandler:^(CMDeviceMotion * _Nullable motion, NSError * _Nullable error) {
        toWrite = [[NSString stringWithFormat:@"%f %f %f", motion.attitude.roll, motion.attitude.pitch, motion.attitude.yaw] dataUsingEncoding:NSUTF8StringEncoding];
        [socket sendData:toWrite withTimeout:-1 tag:0];
    }];
}

- (void)bindTo:(NSString *)address onPort:(int)port {
    NSError *error;
    BOOL success = [socket connectToHost:address onPort:port error:&error];
    if (error || !success) {
        [NSException raise:@"Error connecting to host." format:@"%@", error.description];
    }
}

- (void)bindToDefault {
    [self bindTo:@"localhost" onPort:SERVER_TRANS_PORT];
}
@end
