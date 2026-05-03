#ifndef FRAME_PROCESSOR_HPP
#define FRAME_PROCESSOR_HPP

#include <opencv2/opencv.hpp>
#include <string>
#include <vector>

class FrameProcessor {
public:
    void process(cv::Mat& frame, int mode, float zoom, double angle, const cv::Rect& mouseRect, const std::vector<cv::Rect>& faces = {});
private:
    std::string getModeName(int mode);
};

#endif
