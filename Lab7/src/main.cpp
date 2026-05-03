#include <opencv2/opencv.hpp>
#include <iostream>
#include "CameraProvider.hpp"
#include "FrameProcessor.hpp"
#include "KeyProcessor.hpp"
#include "Display.hpp"
#include "FaceDetector.hpp"

cv::Rect selection(0,0,0,0);
bool isDrawing = false;
int brightnessTrack = 50; 
const std::string winName = "OpenCV Lab";

void onMouse(int event, int x, int y, int flags, void* param) {
    if (event == cv::EVENT_LBUTTONDOWN) {
        isDrawing = true;
        selection = cv::Rect(x, y, 0, 0);
    } else if (event == cv::EVENT_MOUSEMOVE && isDrawing) {
        selection.width = x - selection.x;
        selection.height = y - selection.y;
    } else if (event == cv::EVENT_LBUTTONUP) {
        isDrawing = false;
    }
}

int main() {
    CameraProvider camera(0);
    FrameProcessor processor;
    KeyProcessor keys;
    Display display(winName);
    FaceDetector faceDetector;

    if (!camera.isOpened()) {
        std::cerr << "Error: Camera not found!" << std::endl;
        return -1;
    }

    cv::namedWindow(winName);
    cv::setMouseCallback(winName, onMouse);
    cv::createTrackbar("Brightness", winName, &brightnessTrack, 100);

    float zoom = 1.0f;
    double angle = 0.0;

    while (true) {
        if (cv::getWindowProperty(winName, cv::WND_PROP_VISIBLE) < 1) break;

        cv::Mat frame = camera.getFrame();
        if (frame.empty()) break;

        int beta = (brightnessTrack - 50) * 2;
        frame.convertTo(frame, -1, 1.0, beta);

        int key = cv::waitKey(1);
        if (key == 27) break;

        keys.process(key);
        if (keys.isExitPressed()) break;

        if (key == 82 || key == 'w') zoom += 0.05f;
        if (key == 84 || key == 's') zoom = std::max(0.1f, zoom - 0.05f);
        if (key == 83 || key == 'd') angle += 5.0;
        if (key == 81 || key == 'a') angle -= 5.0;
        if (key == 'r') { zoom = 1.0f; angle = 0.0; selection = cv::Rect(0,0,0,0); }

        std::vector<cv::Rect> currentFaces;
        if (keys.getCurrentMode() == 6) {
            faceDetector.updateFrame(frame);
            currentFaces = faceDetector.getFaces();
        }

        processor.process(frame, keys.getCurrentMode(), zoom, angle, selection, currentFaces);
        display.show(frame);
    }

    cv::destroyAllWindows();
    return 0;
}
