#include "KeyProcessor.hpp"

void KeyProcessor::process(int key) {
    if (key <= 0) return;

    if (key >= '0' && key <= '9') {
        currentMode = key - '0';
    }

    if (key == 27 || key == 113) {
        exitPressed = true;
    }
}
