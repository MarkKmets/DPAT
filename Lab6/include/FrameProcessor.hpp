#ifndef FRAME_PROCESSOR_HPP
#define FRAME_PROCESSOR_HPP

#include <opencv2/opencv.hpp>

class FrameProcessor {
public:
    void process(cv::Mat& frame, int mode, float zoom, double angle, const cv::Rect& mouseRect);
};

#endif
