//
//  RegistrationServer.h
//  maya-client.ios
//
//  Created by Sacha Best on 3/7/16.
//  Copyright © 2016 Sacha Best. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <CocoaAsyncSocket/GCDAsyncSocket.h>

#define SERVER_REG_PORT 9999

@protocol SocketDelegate <NSObject>

- (void)connectionFailed;
- (void)connecttionSuceess;

@end

typedef void(^RegistrationCallback)(void);

@interface RegistrationServer : NSObject <GCDAsyncSocketDelegate> {
    GCDAsyncSocket *socket;
    dispatch_queue_t thread;
    RegistrationCallback callback;
    BOOL connected;
}

@property (weak, nonatomic) NSObject<SocketDelegate>* delegate;

+ (RegistrationServer *)instance;

- (void)bindToDefault;
- (void)bindTo:(NSString *)address onPort:(int)port;
- (void)disconnect;
- (void)registerFrameServer:(int)port withCallback:(RegistrationCallback)block;

- (void)socket:(GCDAsyncSocket *)sender didConnectToHost:(NSString *)host port:(UInt16)port;

@end
