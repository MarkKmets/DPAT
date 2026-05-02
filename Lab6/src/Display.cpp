#include "Display.hpp"

Display::Display(std::string windowName) : name(windowName) {
    cv::namedWindow(name, cv::WINDOW_AUTOSIZE);
}

void Display::show(cv::Mat frame) {
    if (!frame.empty()) {
        cv::imshow(name, frame);
    }
}
