//
//  FrameServer.m
//  maya-client.ios
//
//  Created by Sacha Best on 1/21/16.
//  Copyright © 2016 Sacha Best. All rights reserved.
//

#import "FrameServer.h"

@implementation FrameServer

static FrameServer *instance;

+ (FrameServer *)instance {
    if (!instance) {
        instance = [[FrameServer alloc] init];
    }
    return instance;
}

- (void)connect {
    if (socket || thread) {
        [NSException raise:@"Cannot create socket" format:@"A socket is already open. Please close it before opening a new one. "];
    } else {
        thread = dispatch_queue_create("com.sachabest.maya-client-ios.FrameServer", 0);
        socket = [[GCDAsyncUdpSocket alloc] initWithDelegate:self delegateQueue:thread];
        NSError *error;
        [socket bindToPort:LOCAL_PORT error:&error];
        if (error) {
            [NSException raise:@"Error binding to port." format:@"%@", error.description];
        }
    }
}

- (void)disconnect {
    if (!socket || !thread) {
        return; // nothing to do
    } else {
        [socket close];
        dispatch_suspend(thread);
        socket = NULL;
        thread = NULL;
    }
}
@end
