#!/usr/bin/env python3

# Import the necessary libraries
import time
import math
from ev3dev2.motor import *
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor.virtual import *

# Create the sensors and motors objects
motorA = LargeMotor(OUTPUT_A)
motorB = LargeMotor(OUTPUT_B)
left_motor = motorA
right_motor = motorB
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)

spkr = Sound()
btn = Button()
radio = Radio()
obtr = ObjectTracker()

color_sensor_in1 = ColorSensor(INPUT_1)
ultrasonic_sensor_in2 = UltrasonicSensor(INPUT_2)
gyro_sensor_in3 = GyroSensor(INPUT_3)
gps_sensor_in4 = GPSSensor(INPUT_4)
pen_in5 = Pen(INPUT_5)

motorC = LargeMotor(OUTPUT_C)  # Magnet

from ev3dev2.Training_Wheels import Training_Wheels
training_wheels = Training_Wheels(gps_sensor_in4, gyro_sensor_in3, steering_drive)

# Робота 2, завдання 1: їде вперед і зупиняється за 15 см до перешкоди
tank_drive.on(30, 30)
while ultrasonic_sensor_in2.distance_centimeters > 15:
    time.sleep(0.05)
tank_drive.off()
