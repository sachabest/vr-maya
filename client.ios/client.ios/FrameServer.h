//
//  FrameServer.h
//  maya-client.ios
//
//  Created by Sacha Best on 1/21/16.
//  Copyright © 2016 Sacha Best. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <CocoaAsyncSocket/GCDAsyncUdpSocket.h>

#define SERVER_IP @"10.0.1.10"
#define SERVER_PORT 9999
#define LOCAL_PORT 9999

@interface FrameServer : NSObject {
    GCDAsyncUdpSocket *socket;
    dispatch_queue_t thread;
}

+ (FrameServer *)instance;

@end
