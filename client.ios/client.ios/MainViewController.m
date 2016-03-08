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
    [server bindToDefault];
    [server registerFrameServer:10000 withCallback:^{
        [loadingHUD hide:YES];
        [[FrameServer instance] bindToDefault];
        [[FrameServer instance] registerCallback:^(UIImage *img1, UIImage *img2) {
            dispatch_async(dispatch_get_main_queue(), ^{
                [_imageView1 setImage:img1];
                _imageView1.contentMode = UIViewContentModeScaleAspectFill;
                [_imageView2 setImage:img2];
                _imageView2.contentMode = UIViewContentModeScaleAspectFill;
            });
        }];
    }];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

@end
