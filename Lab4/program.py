import numpy as np
import matplotlib
# Примусово використовуємо TkAgg для гнучкого керування вікном (перенесення меню)
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, filtfilt

# Налаштування базових параметрів
t = np.linspace(0, 10, 1000)
fs = 100  # Частота дискретизації (1000 точок на 10 секунд = 100 Гц)
nyq = 0.5 * fs  # Частота Найквіста

# Початкові значення
INIT_AMP = 1.0
INIT_FREQ = 0.267
INIT_PHASE = 0.0
INIT_NOISE_MEAN = 0.0
INIT_NOISE_COV = 0.1
INIT_CUTOFF = 5.0

# Словник для збереження стану шуму (щоб не перераховувати його без потреби)
noise_state = {
    'mean': INIT_NOISE_MEAN,
    'cov': INIT_NOISE_COV,
    'data': np.random.normal(INIT_NOISE_MEAN, np.sqrt(INIT_NOISE_COV), len(t))
}

# Функції генерації та обробки
def get_noise(mean, cov):
    if mean != noise_state['mean'] or cov != noise_state['cov']:
        noise_state['mean'] = mean
        noise_state['cov'] = cov
        noise_state['data'] = np.random.normal(mean, np.sqrt(max(0, cov)), len(t))
    return noise_state['data']

def apply_filter(data, cutoff):
    cutoff = np.clip(cutoff, 0.1, nyq - 0.1)
    b, a = butter(N=3, Wn=cutoff / nyq, btype='low')
    return filtfilt(b, a, data)

def harmonic_with_noise(amp, freq, phase, noise_mean, noise_cov, cutoff):
    pure_signal = amp * np.sin(2 * np.pi * freq * t + phase)
    noise = get_noise(noise_mean, noise_cov)
    noisy_signal = pure_signal + noise
    filtered_signal = apply_filter(noisy_signal, cutoff)
    return pure_signal, noisy_signal, filtered_signal

# Налаштування графічного інтерфейсу (GUI)
fig, ax = plt.subplots(figsize=(10, 8))
# Додано світлий фон для самого графіка
ax.set_facecolor('#fafafa')
plt.subplots_adjust(left=0.1, bottom=0.45) # Звільняємо місце для слайдерів знизу

# Отримуємо початкові дані
pure_y, noisy_y, filtered_y = harmonic_with_noise(
    INIT_AMP, INIT_FREQ, INIT_PHASE, INIT_NOISE_MEAN, INIT_NOISE_COV, INIT_CUTOFF
)

# Графіки
line_noisy, = ax.plot(t, noisy_y, label='Зашумлена гармоніка', color='lightcoral', alpha=0.8)
line_filtered, = ax.plot(t, filtered_y, label='Відфільтрована', color='darkgreen', linewidth=2.5)
line_pure, = ax.plot(t, pure_y, label='Чиста гармоніка', color='navy', linestyle='--', linewidth=2)

ax.set_xlim(0, 10)
ax.set_ylim(-3, 3)
ax.legend(loc='upper right')
ax.set_title("Генератор гармоніки з шумом та фільтрацією")

# Елементи інтерфейсу (світло-блакитний фон):
axcolor = '#e8f4f8' 
ax_amp    = plt.axes([0.15, 0.35, 0.65, 0.03], facecolor=axcolor)
ax_freq   = plt.axes([0.15, 0.30, 0.65, 0.03], facecolor=axcolor)
ax_phase  = plt.axes([0.15, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_mean   = plt.axes([0.15, 0.20, 0.65, 0.03], facecolor=axcolor)
ax_cov    = plt.axes([0.15, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_cutoff = plt.axes([0.15, 0.10, 0.65, 0.03], facecolor=axcolor)

# Змінено колір самих повзунків на слайдерах
slider_color = 'steelblue'
samp    = Slider(ax_amp, 'Amplitude', 0.1, 3.0, valinit=INIT_AMP, color=slider_color)
sfreq   = Slider(ax_freq, 'Frequency', 0.01, 2.0, valinit=INIT_FREQ, color=slider_color)
sphase  = Slider(ax_phase, 'Phase', 0, 2*np.pi, valinit=INIT_PHASE, color=slider_color)
smean   = Slider(ax_mean, 'Noise Mean', -1.0, 1.0, valinit=INIT_NOISE_MEAN, color=slider_color)
scov    = Slider(ax_cov, 'Noise Covariance', 0.0, 1.0, valinit=INIT_NOISE_COV, color=slider_color)
scutoff = Slider(ax_cutoff, 'Cutoff Frequency', 0.1, 15.0, valinit=INIT_CUTOFF, color=slider_color)

# Створення кнопок та чекбоксів
resetax = plt.axes([0.15, 0.02, 0.1, 0.04])
button_reset = Button(resetax, 'Reset', color=axcolor, hovercolor='#d0e8f0')

checkax = plt.axes([0.7, 0.02, 0.15, 0.05], facecolor=axcolor)
checkbox_noise = CheckButtons(checkax, ['Show Noise'], [True])

# Функції оновлення інтерфейсу
def update(val):
    pure, noisy, filtered = harmonic_with_noise(
        samp.val, sfreq.val, sphase.val, smean.val, scov.val, scutoff.val
    )
    
    line_pure.set_ydata(pure)
    line_noisy.set_ydata(noisy)
    line_filtered.set_ydata(filtered)
    
    # Динамічно підлаштовуємо межі осі Y
    ax.set_ylim(min(noisy.min(), -1.5) - 0.5, max(noisy.max(), 1.5) + 0.5)
    fig.canvas.draw_idle()

def reset(event):
    samp.reset()
    sfreq.reset()
    sphase.reset()
    smean.reset()
    scov.reset()
    scutoff.reset()
    
def toggle_noise(label):
    line_noisy.set_visible(not line_noisy.get_visible())
    fig.canvas.draw_idle()

# Прив'язуємо події до функцій
samp.on_changed(update)
sfreq.on_changed(update)
sphase.on_changed(update)
smean.on_changed(update)
scov.on_changed(update)
scutoff.on_changed(update)

button_reset.on_clicked(reset)
checkbox_noise.on_clicked(toggle_noise)

# ПЕРЕМІЩЕННЯ МЕНЮ НАГОРУ
manager = plt.get_current_fig_manager()
if hasattr(manager, 'toolbar') and hasattr(manager.toolbar, 'pack_forget'):
    # Відкріплюємо елементи і прикріплюємо їх у правильному порядку (меню зверху)
    manager.toolbar.pack_forget()
    manager.canvas.get_tk_widget().pack_forget()
    
    manager.toolbar.pack(side='top', fill='x')
    manager.canvas.get_tk_widget().pack(side='bottom', fill='both', expand=True)

# Запуск програми
plt.show()