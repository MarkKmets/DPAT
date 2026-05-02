#include "FrameProcessor.hpp"
#include <opencv2/imgproc.hpp>

void circshift(cv::Mat& channel, int shift_x) {
    int w = channel.cols;
    shift_x = (shift_x % w + w) % w;
    cv::Mat out = cv::Mat::zeros(channel.size(), channel.type());
    channel(cv::Rect(0, 0, w - shift_x, channel.rows)).copyTo(out(cv::Rect(shift_x, 0, w - shift_x, channel.rows)));
    channel(cv::Rect(w - shift_x, 0, shift_x, channel.rows)).copyTo(out(cv::Rect(0, 0, shift_x, channel.rows)));
    channel = out;
}

std::string getModeName(int mode) {
    switch (mode) {
        case 0: return "Original";
        case 1: return "Inversion";
        case 2: return "Gaussian Blur";
        case 3: return "Canny Edges";
        case 4: return "Glitch Effect";
        case 5: return "Transform (Arrows)";
        default: return "Custom Mode";
    }
}

void FrameProcessor::process(cv::Mat& frame, int mode, float zoom, double angle, const cv::Rect& mouseRect) {
    if (frame.empty()) return;

    if (zoom != 1.0f || angle != 0.0) {
        cv::Mat matrix = cv::getRotationMatrix2D(cv::Point2f(frame.cols/2, frame.rows/2), angle, zoom);
        cv::warpAffine(frame, frame, matrix, frame.size());
    }

    switch (mode) {
        case 1: cv::bitwise_not(frame, frame); break;
        case 2: cv::GaussianBlur(frame, frame, cv::Size(15, 15), 0); break;
        case 3: {
            cv::Mat gray;
            cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
            cv::Canny(gray, gray, 100, 200);
            cv::cvtColor(gray, frame, cv::COLOR_GRAY2BGR);
            break;
        }
        case 4: {
            std::vector<cv::Mat> channels;
            cv::split(frame, channels);
            circshift(channels[0], 25); 
            circshift(channels[2], -25);
            cv::merge(channels, frame);
            break;
        }
    }

    if (mouseRect.width != 0) {
        cv::rectangle(frame, mouseRect, cv::Scalar(0, 255, 0), 2);
    }

    std::string info = "Mode " + std::to_string(mode) + ": " + getModeName(mode);
    cv::putText(frame, info, cv::Point(20, 40), cv::FONT_HERSHEY_SIMPLEX, 0.8, cv::Scalar(0, 255, 255), 2);
}
