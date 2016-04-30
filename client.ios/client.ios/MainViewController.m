//
//  ViewController.m
//  client.ios
//
//  Created by Sacha Best on 1/21/16.
//  Copyright © 2016 Sacha Best. All rights reserved.
//

#import "MainViewController.h"
#import "FrameServer.h"
#import "RegistrationServer.h"
#import "TransformServer.h"

@interface MainViewController ()

@end

@implementation MainViewController

- (void)viewDidLoad {
    [super viewDidLoad];

    // Do any additional setup after loading the view, typically from a nib.
}

- (void)viewDidAppear:(BOOL)animated {
    M13ProgressView *loadingView = [[M13ProgressViewRing alloc] init];
    loadingHUD = [[M13ProgressHUD alloc] initAndShowWithProgressView:loadingView progress:0.5 indeterminate:YES status:@"Searching..." mask:M13ProgressHUDMaskTypeGradient inView:self.view];
    loadingHUD.progressViewSize = CGSizeMake(60.0f, 60.0f);
    RegistrationServer *server = [RegistrationServer instance];
//    [server bindToDefault];
    UIAlertController *alert = [UIAlertController alertControllerWithTitle:@"Enter IP" message:@"Please enter the IP address of the server." preferredStyle:UIAlertControllerStyleAlert];
    [alert addTextFieldWithConfigurationHandler:^(UITextField * _Nonnull textField) {
        textField.placeholder = @"IP Address";
    }];
    UIAlertAction* defaultAction = [UIAlertAction actionWithTitle:@"OK" style:UIAlertActionStyleDefault handler:^(UIAlertAction * action) {
//        [server bindTo:alert.textFields[0].text onPort:SERVER_PORT];
        [server bindToDefault];
        [server registerFrameServer:10000 withCallback:^{
            dispatch_async(dispatch_get_main_queue(), ^{
                [loadingHUD hide:YES];
            });
            [[FrameServer instance] bindToDefault];
            [[FrameServer instance] registerCallback:^(UIImage *img1, UIImage *img2) {
                dispatch_async(dispatch_get_main_queue(), ^{
                    [_imageView1 setImage:img1];
                    _imageView1.contentMode = UIViewContentModeScaleAspectFill;
                    [_imageView2 setImage:img2];
                    _imageView2.contentMode = UIViewContentModeScaleAspectFill;
                });
            }];
            [[TransformServer instance] bindToDefault];
            [[TransformServer instance] startSendingData];
        }];
    }];
    [alert addAction:defaultAction];
    [self presentViewController:alert animated:YES completion:NULL];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

@end
