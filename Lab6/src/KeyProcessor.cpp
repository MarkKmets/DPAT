#include "KeyProcessor.hpp"

void KeyProcessor::process(int key) {
    if (key <= 0) return;

    // Клавіші 0-9 змінюють режим
    if (key >= '0' && key <= '9') {
        currentMode = key - '0'; // Перетворюємо символ цифри у число 0-9
    }

    // Клавіші Esc (27) або 'q' (113) для виходу
    if (key == 27 || key == 113) {
        exitPressed = true;
    }
}
