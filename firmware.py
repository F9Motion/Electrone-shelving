from machine import Pin, PWM, ADC, I2C
from neopixel import NeoPixel
import time
import ssd1306   # установить: Thonny -> Инструменты -> Управление пакетами -> micropython-ssd1306
 
# ====================== НАСТРОЙКИ (ПРОВЕРЬ ПО СХЕМЕ) ======================
# Это номера GPIO (число после "IO" на схеме), а не номера выводов корпуса.
LED_PIN = 0        # IO0 -> DIN первого WS2812B (через R4)
BTN_NEXT_PIN = 1   # IO1 -> SW1 (вперёд)
BTN_PREV_PIN = 2   # IO2 -> SW2 (назад)
SCL_PIN = 3        # IO3 -> SCL экрана
SDA_PIN = 4        # IO4 -> SDA экрана
BUZZER_PIN = 7     # ПРОВЕРЬ: к какому IO подключён BZ1
BATTERY_PIN = 5    # ПРОВЕРЬ: к какому IO подключено измерение батареи
 
LED_COUNT = 6
OLED_ADDR = 0x3C
OLED_W, OLED_H = 128, 32
 
DIVIDER_RATIO = 2.0    # во сколько раз делитель уменьшает напряжение батареи
V_EMPTY = 3.0          # 0% заряда, вольт
V_FULL = 4.2           # 100% заряда, вольт
LOW_BATTERY = 5        # ниже этого процента пищит buzzer
 
SCREEN_TIMEOUT_MS = 15000
LONG_PRESS_MS = 1000
DOUBLE_CLICK_MS = 350
DEBOUNCE_MS = 30
# ==========================================================================
 
# ---------- цвета ----------
colors = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 100, 120),
    (120, 120, 0), (255, 255, 255), (100, 0, 120),
]
names = ["red", "green", "blue", "aqua", "yellow", "white", "pink"]
 
 
def apply_brightness(color, percentage):
    return (int(color[0] * percentage / 100),
            int(color[1] * percentage / 100),
            int(color[2] * percentage / 100))
 
 
# ---------- железо ----------
np = NeoPixel(Pin(LED_PIN), LED_COUNT)
 
i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)
oled = ssd1306.SSD1306_I2C(OLED_W, OLED_H, i2c, OLED_ADDR)
 
buzzer = PWM(Pin(BUZZER_PIN), freq=2000, duty_u16=0)
 
adc = ADC(Pin(BATTERY_PIN), atten=ADC.ATTN_11DB)
 
 
def set_all(color):
    for i in range(LED_COUNT):
        np[i] = color
    np.write()
 
 
def read_battery_percent():
    total = 0
    for _ in range(8):
        total += adc.read_uv()
    volts = (total / 8) / 1000000 * DIVIDER_RATIO
    percent = (volts - V_EMPTY) / (V_FULL - V_EMPTY) * 100
    return max(0, min(100, int(percent)))
 
 
# ---------- кнопка: короткое / двойное / долгое нажатие ----------
class Button:
    def __init__(self, pin_number):
        self.pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
        self.pressed = False
        self.last_change = 0
        self.press_time = 0
        self.last_release = 0
        self.clicks = 0
        self.long_fired = False
 
    def update(self):
        """Возвращает None, 'single', 'double' или 'long'."""
        now = time.ticks_ms()
        down = self.pin.value() == 0
        event = None
 
        if down != self.pressed and time.ticks_diff(now, self.last_change) > DEBOUNCE_MS:
            self.last_change = now
            self.pressed = down
            if down:
                self.press_time = now
                self.long_fired = False
            elif not self.long_fired:
                self.clicks += 1
                self.last_release = now
 
        if self.pressed and not self.long_fired and \
                time.ticks_diff(now, self.press_time) >= LONG_PRESS_MS:
            self.long_fired = True
            self.clicks = 0
            event = "long"
 
        if self.clicks and not self.pressed and \
                time.ticks_diff(now, self.last_release) >= DOUBLE_CLICK_MS:
            event = "double" if self.clicks >= 2 else "single"
            self.clicks = 0
 
        return event
 
 
btn_next = Button(BTN_NEXT_PIN)
btn_prev = Button(BTN_PREV_PIN)
 
# ---------- состояние ----------
index = 0
brightness = 30
lamps_on = True
battery = read_battery_percent()
 
screen_on = True
last_activity = time.ticks_ms()
last_screen_update = 0
last_battery_read = time.ticks_ms()
 
 
def refresh_leds():
    if lamps_on:
        set_all(apply_brightness(colors[index], brightness))
    else:
        set_all((0, 0, 0))
 
 
def draw_screen():
    oled.fill(0)
    if screen_on:
        oled.text(names[index], 0, 0)
        oled.text("Bat: " + str(battery) + "%", 0, 11)
        oled.text("Bright: " + str(brightness) + "%" + ("" if lamps_on else " OFF"), 0, 22)
    oled.show()
 
 
def handle_event(event, direction):
    """direction: +1 для SW1, -1 для SW2."""
    global index, brightness, lamps_on
    if event == "single":
        index = (index + direction) % len(colors)
    elif event == "double":
        brightness = max(10, min(100, brightness + 10 * direction))
    elif event == "long":
        lamps_on = not lamps_on
    refresh_leds()
 
 
refresh_leds()
draw_screen()
 
# ---------- главный цикл ----------
while True:
    now = time.ticks_ms()
 
    ev1 = btn_next.update()
    ev2 = btn_prev.update()
 
    if btn_next.pressed or btn_prev.pressed or ev1 or ev2:
        last_activity = now
        if not screen_on:
            screen_on = True
            draw_screen()
 
    if ev1:
        handle_event(ev1, +1)
        draw_screen()
    if ev2:
        handle_event(ev2, -1)
        draw_screen()
 
    # гасим экран после 15 секунд бездействия
    if screen_on and time.ticks_diff(now, last_activity) > SCREEN_TIMEOUT_MS:
        screen_on = False
        draw_screen()
 
    # замер батареи раз в 2 секунды
    if time.ticks_diff(now, last_battery_read) > 2000:
        last_battery_read = now
        battery = read_battery_percent()
        if screen_on:
            draw_screen()
 
    # buzzer: короткий писк раз в 2 секунды при заряде ниже порога
    if battery < LOW_BATTERY and (now % 2000) < 200:
        buzzer.duty_u16(32768)
    else:
        buzzer.duty_u16(0)
 
    time.sleep_ms(10)
 