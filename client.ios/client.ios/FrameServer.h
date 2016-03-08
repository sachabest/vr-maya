//
//  FrameServer.h
//  maya-client.ios
//
//  Created by Sacha Best on 1/21/16.
//  Copyright © 2016 Sacha Best. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>
#import <CocoaAsyncSocket/GCDAsyncSocket.h>

#define SERVER_IP @"localhost"
#define SERVER_PORT 10000
#define LOCAL_PORT 9999

#define TAG_FRAME_1 0
#define TAG_FRAME_2 1
#define TAG_FRAME_LENGTH 2

typedef void(^FrameCallback)(UIImage *, UIImage *);

@interface FrameServer : NSObject <GCDAsyncSocketDelegate> {
    GCDAsyncSocket *socket;
    GCDAsyncSocket *connection;
    dispatch_queue_t thread;
    FrameCallback callback;
    long nextImageLength;
    bool frame2;
    UIImage *img1;
    UIImage *img2;
}

+ (FrameServer *)instance;

- (void)bindToDefault;
- (void)bindTo:(NSString *)address onPort:(int)port;

- (void)registerCallback:(FrameCallback) block;

@end
