//
//  ViewController.h
//  client.ios
//
//  Created by Sacha Best on 1/21/16.
//  Copyright © 2016 Sacha Best. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <M13ProgressSuite/M13ProgressHUD.h>
#import <M13ProgressSuite/M13ProgressViewRing.h>

@interface MainViewController : UIViewController {
    M13ProgressHUD *loadingHUD;
}

@property (weak, nonatomic) IBOutlet UIImageView *imageView1;
@property (weak, nonatomic) IBOutlet UIImageView *imageView2;

@end

