#ifndef KEY_PROCESSOR_HPP
#define KEY_PROCESSOR_HPP

#include <opencv2/opencv.hpp>

class KeyProcessor {
public:
    KeyProcessor() : currentMode(0), exitPressed(false) {}

    // Метод для обробки клавіш
    void process(int key);

    // Гетери для основної логіки
    int getCurrentMode() const { return currentMode; }
    bool isExitPressed() const { return exitPressed; }

private:
    int currentMode;
    bool exitPressed;
};

#endif
