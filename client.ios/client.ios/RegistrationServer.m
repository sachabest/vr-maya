//
//  RegistrationServer.m
//  maya-client.ios
//
//  Created by Sacha Best on 3/7/16.
//  Copyright © 2016 Sacha Best. All rights reserved.
//

#import "RegistrationServer.h"

@implementation RegistrationServer

static RegistrationServer *instance;

+ (RegistrationServer *)instance {
    if (!instance) {
        instance = [[RegistrationServer alloc] init];
        [instance create];
    }
    return instance;
}

- (void)create {
    if (socket || thread) {
        [NSException raise:@"Cannot create socket" format:@"A socket is already open. Please close it before opening a new one. "];
    } else {
//        thread = dispatch_get_main_queue();
        thread = dispatch_queue_create("com.sachabest.maya-client-ios.RegistrationServer", 0);
        socket = [[GCDAsyncSocket alloc] initWithDelegate:instance delegateQueue:thread];
    }
}

// address unused for now
- (void)bindTo:(NSString *)address onPort:(int)port {
    NSError *error;
    BOOL success = [socket connectToHost:address onPort:port error:&error];
    if (error || !success) {
        [NSException raise:@"Error connecting to host." format:@"%@", error.description];
    }
}

- (void)bindToDefault {
    [self bindTo:@"localhost" onPort:SERVER_REG_PORT];
}

- (void)registerFrameServer:(int)port withCallback:(RegistrationCallback)block {
    callback = block;
    [socket writeData:[[NSString stringWithFormat:@"%d\n", port] dataUsingEncoding:NSUTF8StringEncoding] withTimeout:-1 tag:0];
    [socket readDataWithTimeout:-1 tag:0];
}

- (void)disconnect {
    if (!socket || !thread) {
        return; // nothing to do
    } else {
        [socket disconnect];
        connected = false;
        dispatch_suspend(thread);
        socket = NULL;
        thread = NULL;
    }
}

- (void)socketDidDisconnect:(GCDAsyncSocket *)sock withError:(NSError *)err {
    NSLog(@"%@", err);
    if (_delegate) {
        [_delegate connectionFailed];
    }
    connected = false;
}

- (void)socket:(GCDAsyncSocket *)sender didConnectToHost:(NSString *)host port:(UInt16)port {
    NSLog(@"Woo we connected!");
    if (_delegate) {
        [_delegate connecttionSuceess];
    }
    connected = true;
}

- (void)socket:(GCDAsyncSocket *)sender didReadData:(NSData *)data withTag:(long)tag {
    NSString *recv = [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding];
    if (![recv isEqual:@"ok"]) {
        [NSException raise:@"Couldn't connect to host." format:@""];
    }
    [self disconnect];
    callback();
}

@end
