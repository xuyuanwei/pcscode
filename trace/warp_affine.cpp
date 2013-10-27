/*
 * reference: http://www.opencv.org.cn/opencvdoc/2.3.2/html/doc/tutorials/imgproc/imgtrans/warp_affine/warp_affine.html 
 * keyword: affineTransform 仿射变化; perspectiveTransform 透视变化
 */
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>

using namespace cv;
using namespace std;

/// 全局变量
char source_window[] = "Source image";
char warp_window[] = "Warp";
char warp_rotate_window[] = "Warp + Rotate";
char perspective_window[] = "perspective transform";

/** @function main */
int main( int argc, char** argv )
{
    Point2f srcTri[3];
    Point2f dstTri[3];

    Point2f srcTri_perspective[4];
    Point2f dstTri_perspective[4];

    Mat rot_mat( 2, 3, CV_32FC1 );
    Mat warp_mat( 2, 3, CV_32FC1 );
    Mat src, warp_dst, warp_rotate_dst;

    Mat perspective_mat(3,3,CV_32FC1);
    Mat perspective_dst;
    Mat perspective_dst_xoffset;

    /// 加载源图像
    src = imread( argv[1], 1 );
    if(!src.data)
    {
        cout << "imread fail"<<endl;
        return -1;
    }

    /// 设置目标图像的大小和类型与源图像一致
    warp_dst = Mat::zeros( src.rows, src.cols, src.type() );
    //perspective_dst=Mat::zeros(src.rows*2, src.cols*2, src.type() );
    perspective_dst=Mat::zeros(480, 1280, src.type() );

    /*
    /// 设置源图像和目标图像上的三组点以计算仿射变换
    srcTri[0] = Point2f( 0,0 );
    srcTri[1] = Point2f( src.cols - 1, 0 );
    srcTri[2] = Point2f( 0, src.rows - 1 );

    dstTri[0] = Point2f( src.cols*0.0, src.rows*0.33 );
    dstTri[1] = Point2f( src.cols*0.85, src.rows*0.25 );
    dstTri[2] = Point2f( src.cols*0.15, src.rows*0.7 );

    /// 求得仿射变换
    warp_mat = getAffineTransform( srcTri, dstTri );

    /// 对源图像应用上面求得的仿射变换
    warpAffine( src, warp_dst, warp_mat, warp_dst.size() );

    namedWindow( source_window, CV_WINDOW_AUTOSIZE );
    imshow( source_window, src );

    namedWindow( warp_window, CV_WINDOW_AUTOSIZE );
    imshow( warp_window, warp_dst );
    */

    /*
     * source
       0.3:    140,628      558,628
       0.6:    140,558      558,558
       1:      140,465      558,465
       2:      140,233      558,233
       3:      140,1        558,1

       distination
        0.3:    38,242      501,242
        0.6:    96,173      444,173
        1:      140,120     401,120
        2:      189,62      354,62
        3:      211,36      332,37
        */
    int x_offset=350;

    srcTri_perspective[0] = Point2f( 140,628 );
    srcTri_perspective[1] = Point2f( 558,628 );
    srcTri_perspective[2] = Point2f( 140,1  );
    srcTri_perspective[3] = Point2f( 558,1  );

    dstTri_perspective[0] = Point2f( 38+x_offset,242  );
    dstTri_perspective[1] = Point2f( 501+x_offset,242 );
    dstTri_perspective[2] = Point2f( 211+x_offset,36  );
    dstTri_perspective[3] = Point2f( 332+x_offset,37  );

    /* TODO: try findHomography function */
    perspective_mat=getPerspectiveTransform(srcTri_perspective,dstTri_perspective);
    //cout << perspective_mat <<endl;
    warpPerspective(src,perspective_dst,perspective_mat,perspective_dst.size());

    imwrite("output.bmp",perspective_dst);
    namedWindow( warp_window, CV_WINDOW_AUTOSIZE );
    imshow( perspective_window, perspective_dst);

    /* create offset */
    /*
    srcTri_perspective[0] = Point2f( 0,0  );
    srcTri_perspective[1] = Point2f( 100,0);
    srcTri_perspective[2] = Point2f( 0,100  );
    srcTri_perspective[3] = Point2f( 100,100);

    dstTri_perspective[0] = Point2f( 0+x_offset,0  );
    dstTri_perspective[1] = Point2f( 100+x_offset,0 );
    dstTri_perspective[2] = Point2f( 0+x_offset,100  );
    dstTri_perspective[3] = Point2f( 100+x_offset,100  );

    perspective_mat=getPerspectiveTransform(srcTri_perspective,dstTri_perspective);
    cout << perspective_mat <<endl;
    warpPerspective(perspective_dst,perspective_dst_xoffset,perspective_mat,perspective_dst.size());
    imwrite("output.bmp",perspective_dst_xoffset);
    namedWindow( warp_window, CV_WINDOW_AUTOSIZE );
    imshow( perspective_window, perspective_dst_xoffset);
    */


    /** 对图像扭曲后再旋转 */

    /*
    /// 计算绕图像中点顺时针旋转50度缩放因子为0.6的旋转矩阵
    Point center = Point( warp_dst.cols/2, warp_dst.rows/2 );
    double angle = -50.0;
    double scale = 0.6;

    /// 通过上面的旋转细节信息求得旋转矩阵
    rot_mat = getRotationMatrix2D( center, angle, scale );

    /// 旋转已扭曲图像
    warpAffine( warp_dst, warp_rotate_dst, rot_mat, warp_dst.size() );

    /// 显示结果
    namedWindow( source_window, CV_WINDOW_AUTOSIZE );
    imshow( source_window, src );

    namedWindow( warp_window, CV_WINDOW_AUTOSIZE );
    imshow( warp_window, warp_dst );

    namedWindow( warp_rotate_window, CV_WINDOW_AUTOSIZE );
    imshow( warp_rotate_window, warp_rotate_dst );
    */

    /// 等待用户按任意按键退出程序
    waitKey(0);

    return 0;
}
