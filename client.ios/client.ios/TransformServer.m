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
        movementDirections = [[NSMutableArray alloc] initWithCapacity:3];
        previousVelocity = [[NSMutableArray alloc] initWithCapacity:3];
        directionValid = [[NSMutableArray alloc] initWithCapacity:3];
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

- (NSArray *)accel:(NSArray *)delta {
    NSMutableArray *ret = [[NSMutableArray alloc] initWithCapacity:delta.count];
    for (int i = 0; i < delta.count; i++) {
        NSNumber *d = [NSNumber numberWithDouble:[delta[i] floatValue] / dt];
        ret[i] = d;
    }
    return ret;
}

float rad2deg(float input) {
    return input * 180.0f / M_PI;
}

- (void)startSendingData {
    [gyroManager startDeviceMotionUpdatesToQueue:gyroQueue withHandler:^(CMDeviceMotion * _Nullable motion, NSError * _Nullable error) {
        double old_t = t;
        dt = [[NSDate date] timeIntervalSince1970] - old_t;
        t = dt + old_t;
        NSMutableArray *toSend = [@[ [NSNumber numberWithDouble:motion.attitude.pitch], [NSNumber numberWithDouble:motion.attitude.yaw], [NSNumber numberWithDouble:motion.attitude.roll]] mutableCopy];
        NSArray *currentVelocity = @[ [NSNumber numberWithDouble:motion.rotationRate.x], [NSNumber numberWithDouble:motion.rotationRate.y], [NSNumber numberWithDouble:motion.rotationRate.z]];
        NSArray *delta = [self delta:currentVelocity old:previousVelocity];
        NSArray *accel = [self accel:delta];
        
        for (int i = 0; i < currentVelocity.count; i++) {
            NSNumber *direction = [NSNumber numberWithDouble:[currentVelocity[i] floatValue] / fabs([currentVelocity[i] floatValue])];
            if (movementDirections[i] && [movementDirections[i] floatValue] * [direction floatValue] > 0) {
                // we are moving same direction
                // now, how can we use acceleration to predict the next movement step
                toSend[i] = [NSNumber numberWithDouble:[toSend[i] floatValue] + ([currentVelocity[i] floatValue] * dt)];
                // integrate second order continuity later
            } else {
                // we are moving different direction, reset and do not predict
                movementDirections[i] = [NSNumber numberWithDouble:[movementDirections[i] floatValue] * -1];
            }
        }
        
        // use dt to estimate next rotation values via 2nd order continuity assumptions
        // i.e. we assume the next dt will be the same as this one, so we have acceleration
        // for each value, we have p2 = p1 +
        
        
        NSData *data = [[NSString stringWithFormat:@"%f %f %f", rad2deg([toSend[0] floatValue]), rad2deg([toSend[1] floatValue]), rad2deg([toSend[2] floatValue])] dataUsingEncoding:NSUTF8StringEncoding];
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
