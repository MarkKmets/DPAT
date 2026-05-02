#include "CameraProvider.hpp"

CameraProvider::CameraProvider(int deviceId) {
    cap.open(deviceId);
}

cv::Mat CameraProvider::getFrame() {
    cv::Mat frame;
    if (cap.isOpened()) {
        cap >> frame;
    }
    return frame;
}

bool CameraProvider::isOpened() {
    return cap.isOpened();
}
