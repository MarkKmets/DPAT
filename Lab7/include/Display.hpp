#pragma once
#include <opencv2/opencv.hpp>
#include <string>

class Display {
public:
    Display(std::string windowName);
    void show(cv::Mat frame);
private:
    std::string name;
};
