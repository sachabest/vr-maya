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
        [instance create];
    }
    return instance;
}

- (void)create {
    if (socket || thread) {
        [NSException raise:@"Cannot create socket" format:@"A socket is already open. Please close it before opening a new one. "];
    } else {
        thread = dispatch_queue_create("com.sachabest.maya-client-ios.FrameServer", 0);
        socket = [[GCDAsyncSocket alloc] initWithDelegate:instance delegateQueue:thread];
    }
}

- (void)bindToDefault {
    [self bindTo:@"localhost" onPort:SERVER_PORT];
}

// address unused for now
- (void)bindTo:(NSString *)address onPort:(int)port {
    NSError *error;
    [socket acceptOnPort:port error:&error];
    if (error) {
        [NSException raise:@"Error binding to port." format:@"%@", error.description];
    } else {
        NSLog(@"Server running on port 10000");
    }
}

- (void)registerCallback:(FrameCallback)block {
    callback = block;
}

- (void)disconnect {
    if (!socket || !thread) {
        return; // nothing to do
    } else {
        [socket disconnect];
        [connection disconnect];
        dispatch_suspend(thread);
        socket = NULL;
        thread = NULL;
    }
}

- (NSData *)socketData:(NSString *)data {
    NSMutableData *mutable = [[[data stringByAppendingString:@"\r\n"] dataUsingEncoding:NSUTF8StringEncoding] mutableCopy];
    return mutable;
}

- (void)socket:(GCDAsyncSocket *)sender didReadData:(NSData *)data withTag:(long)tag {
    switch (tag) {
        case TAG_FRAME_LENGTH:
            nextImageLength = [[[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding] intValue]; // + 8; // 8 byte buffer zone is ONLY NECESSARY IN PYTHON DAMMIT
            [sender writeData:[self socketData:@"k"] withTimeout:-1 tag:frame2 ? TAG_FRAME_2 : TAG_FRAME_1];
            break;
        case TAG_FRAME_1:
            img1 = [UIImage imageWithData:data];
            frame2 = true;
            [sender writeData:[self socketData:@"k"] withTimeout:-1 tag:TAG_FRAME_LENGTH];
            break;
        case TAG_FRAME_2:
            img2 = [UIImage imageWithData:data];
            frame2 = false;
            [sender writeData:[self socketData:@"k"] withTimeout:-1 tag:TAG_FRAME_LENGTH];
            callback(img1, img2);
            break;
        default:
            break;
    }
}

- (void)socket:(GCDAsyncSocket *)sock didWriteDataWithTag:(long)tag {
    switch (tag) {
        case TAG_FRAME_1:
            [sock readDataToLength:nextImageLength withTimeout:-1 tag:TAG_FRAME_1];
            break;
        case TAG_FRAME_2:
            [sock readDataToLength:nextImageLength withTimeout:-1 tag:TAG_FRAME_2];
            break;
        case TAG_FRAME_LENGTH:
            [sock readDataWithTimeout:-1 tag:TAG_FRAME_LENGTH];
            break;
    }
}

- (void)socket:(GCDAsyncSocket *)sock didWritePartialDataOfLength:(NSUInteger)partialLength tag:(long)tag {
    NSLog(@"wrote partial data.");
}

- (void)socket:(GCDAsyncSocket *)sender didAcceptNewSocket:(GCDAsyncSocket *)newSocket {
    NSLog(@"Cool, I'm listening! That was easy.");
    connection = newSocket;
    connection.delegate = self;
    [connection readDataWithTimeout:-1 tag:TAG_FRAME_LENGTH];
}

- (void)socket:(GCDAsyncSocket *)sender didConnectToHost:(NSString *)host port:(UInt16)port {
    NSLog(@"Cool, I'm connected! That was easy.");
}

- (void)socketDidDisconnect:(GCDAsyncSocket *)sock withError:(NSError *)err {
    NSLog(@"%@", err);
}

@end
