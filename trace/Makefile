GCC=cpp

# get from pkgconfig --cflags --libs opencv
INCLUDEFLAG=-I/usr/include/opencv
LIBFLAG=-lopencv_core -lopencv_imgproc -lopencv_highgui -lopencv_ml -lopencv_video -lopencv_features2d -lopencv_calib3d -lopencv_objdetect -lopencv_contrib -lopencv_legacy -lopencv_flann 

default: warp_affine.cpp
	$(GCC) $(INCLUDEFLAG) $(LIBFLAG) -g -o test.o warp_affine.cpp

