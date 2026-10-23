from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor
import time

tank = MoveTank(OUTPUT_A, OUTPUT_B)
ultra = UltrasonicSensor(INPUT_2)     # у Gears порт обов'язковий
gyro = GyroSensor(INPUT_3)
time.sleep(0.5)

# Місія 3 · ускладнення 1: довезти вантаж у зону B за 90 с.
# Фрагмент для відео: дістатися до зони B (стіна) і розвернутись на базу.
LIMIT = 90                            # жорсткий ліміт часу місії, с
start_misii = time.time()

stan = "poshuk"
vkhid = time.time()                   # коли увійшли в поточний стан


def perekhid(novyi):
    """Єдине місце, де змінюється стан: друк і дії при вході."""
    global stan, vkhid
    print("%s -> %s  (t=%.1f с)" % (stan, novyi, time.time() - start_misii))
    stan = novyi
    vkhid = time.time()
    if novyi == "rozvorot":
        gyro.reset()                  # скинути гіроскоп при вході в поворот


while stan != "gotovo":
    d = ultra.distance_centimeters

    if stan == "poshuk":              # їдемо до зони B
        tank.on(SpeedPercent(30), SpeedPercent(30))
        if d < 45:
            perekhid("pidhid")

    elif stan == "pidhid":            # наближаємось до зони B повільно
        tank.on(SpeedPercent(10), SpeedPercent(10))
        if d < 15:
            perekhid("rozvorot")

    elif stan == "rozvorot":          # розвертаємось на місці
        tank.on(SpeedPercent(20), SpeedPercent(-20))
        if gyro.angle >= 180:
            tank.off()
            perekhid("gotovo")

    if time.time() - start_misii > LIMIT:   # ускладнення 1: ліміт часу місії
        print("ліміт часу %d с вийшов у стані %s" % (LIMIT, stan))
        tank.off()
        break

    if time.time() - vkhid > 20:      # таймаут: стан без виходу
        print("таймаут у стані", stan)
        tank.off()
        break

print("кінець, стан:", stan)
