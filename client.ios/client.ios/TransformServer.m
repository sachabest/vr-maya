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
        storedData = [[NSMutableArray alloc] initWithCapacity:3];
        for (int i = 0; i < 3; i++) {
            storedData[i] = [[NSMutableArray alloc] init];
        }
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

- (NSArray *)delta:(NSArray *)a1 old:(NSArray *)a2 {
    NSMutableArray *delta = [[NSMutableArray alloc] initWithCapacity:a1.count];
    for (int i = 0; i < a1.count; i++) {
        NSNumber *n1 = a1[i];
        NSNumber *n2 = a2[i];
        NSNumber *d = [NSNumber numberWithDouble:[n1 floatValue] - [n2 floatValue]];
        delta[i] = d;
    }
    return delta;
}

float rad2deg(float input) {
    return input * 180.0f / M_PI;
}

- (void)startSendingData {
    [gyroManager startDeviceMotionUpdatesToQueue:gyroQueue withHandler:^(CMDeviceMotion * _Nullable motion, NSError * _Nullable error) {
//        double old_t = t;
//        dt = [[NSDate date] timeIntervalSince1970] - old_t;
//        t = dt + old_t;
//        
//        NSArray *currentVelocity = @[ [NSNumber numberWithDouble:motion.rotationRate.x], [NSNumber numberWithDouble:motion.rotationRate.y], [NSNumber numberWithDouble:motion.rotationRate.z]];
//        NSArray *delta = [self delta:currentVelocity old:previousVelocity];
//        
//        bool estimate = true;
//        
//        // first we should see if the second derivative is positive to ensure continuous movement
//        for (int i = 0; i < 3; i++) {
//            if ([((NSNumber *)delta[i]) floatValue] < 0) {
//                estimate = false;
//                break;
//            }
//        }
        
        // use dt to estimate next rotation values via 2nd order continuity assumptions
        // i.e. we assume the next dt will be the same as this one, so we have acceleration
        // for each value, we have p2 = p1 +
        
        
        NSData *data = [[NSString stringWithFormat:@"%f %f %f", rad2deg(motion.attitude.roll), rad2deg(motion.attitude.pitch), rad2deg(motion.attitude.yaw)] dataUsingEncoding:NSUTF8StringEncoding];
        [socket sendData:data withTimeout:-1 tag:0];
    }];
}

- (void)udpSocket:(GCDAsyncUdpSocket *)sock didConnectToAddress:(NSData *)address {
    NSLog(@"UDP Connected!");
}
- (void)udpSocket:(GCDAsyncUdpSocket *)sock didSendDataWithTag:(long)tag {
//    NSLog(@"Data sent!");
}
- (void)udpSocket:(GCDAsyncUdpSocket *)sock didNotConnect:(NSError *)error {
    NSLog(@"UDP Could not connect!");
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
