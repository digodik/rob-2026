from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.virtual import GPSSensor
import time

tank = MoveTank(OUTPUT_A, OUTPUT_B)
color = ColorSensor(INPUT_1) # у Gears порт обов'язковий
gps = GPSSensor(INPUT_4) # лише щоб зупинити секундомір на фініші
time.sleep(0.5)

PORIH = 50 # з роботи 4: біле 100, чорне 1

def obmezhyty(v):
    """SpeedPercent поза ±100 у Gears падає з ValueError."""
    return max(-100, min(100, v))

# Робота 5, кроки 3-5: П-регулятор (Simple Curves)
# пробував Kp: 0.5, 1, 2, 3, 3.5, 4 (на 4 розгойдування, не доїхав)
# обраний Kp = 2, прогони: 22.1 / 21.9 / 21.7 с
BAZA = 20
Kp = 2

pochatok = time.time()
sum_e = 0
n = 0
perehody = 0
znak_pop = 0
while time.time() - pochatok < 120 and gps.y < 85:
    v = color.reflected_light_intensity
    e = PORIH - v
    korekciya = Kp * e
    tank.on(SpeedPercent(obmezhyty(BAZA - korekciya)),
            SpeedPercent(obmezhyty(BAZA + korekciya)))
    # трохи статистики, щоб описати рух числами, а не на око
    sum_e += abs(e)
    n += 1
    znak = 1 if e > 0 else -1
    if znak_pop != 0 and znak != znak_pop:
        perehody += 1  # e змінила знак = робот перелетів межу лінії
    znak_pop = znak

tank.off()
print("час до кінця траси: %.1f с" % (time.time() - pochatok))
print("y кінець", round(gps.y, 1), "| середня |e|:", round(sum_e / max(n, 1), 1), "| перетинів лінії:", perehody)
