//
//  TransformServer.h
//  maya-client.ios
//
//  Created by Sacha Best on 4/28/16.
//  Copyright © 2016 Sacha Best. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <CocoaAsyncSocket/GCDAsyncUdpSocket.h>
#import <CoreMotion/CoreMotion.h>

#define SERVER_TRANS_PORT 10001

@interface TransformServer : NSObject <GCDAsyncUdpSocketDelegate> {
    GCDAsyncUdpSocket *socket;
    dispatch_queue_t thread;
    CMMotionManager *gyroManager;
    NSOperationQueue *gyroQueue;
    NSData *toWrite;
}


+ (TransformServer *)instance;

- (void)bindToDefault;
- (void)bindTo:(NSString *)address onPort:(int)port;
- (void)startSendingData;

@end
