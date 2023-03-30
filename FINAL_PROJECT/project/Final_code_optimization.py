from utils.brick import (
    TouchSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick,
    Motor, EV3ColorSensor)
from time import sleep, time
from math import sqrt
from RGB import color_choosing

wait_ready_sensors(True)

MOTORS = {
    'LEFT': Motor('D'),
    'RIGHT': Motor('A'),
    'DELIVERY': Motor('C'),
    'PUSHING': Motor('B')
}

SENSORS = {
    'LINE': EV3ColorSensor(3),
    'COLOR': EV3ColorSensor(2),
    'TOUCH': TouchSensor(4)
}

BASE_SPEED = 20
DELIVERY_ANGLES = [60, 90, 120, 150, 180, 210]


def set_motor_power(left_power, right_power):
    MOTORS['LEFT'].set_power(left_power)
    MOTORS['RIGHT'].set_power(right_power)


def move(line_sensor_value, is_forward):
    speed_adjustment = 20 if is_forward else -20
    color = color_choosing(line_sensor_value)

    if color == 1:
        set_motor_power(BASE_SPEED, BASE_SPEED + speed_adjustment)
    elif color == 3:
        set_motor_power(BASE_SPEED + speed_adjustment, BASE_SPEED)
    else:
        set_motor_power(BASE_SPEED, BASE_SPEED)


def timed_loop_motor(duration=1, power=20):
    endtime = time() + duration
    while time() < endtime:
        MOTORS['PUSHING'].set_power(power)


def delivery_protocol(degrees):
    MOTORS['DELIVERY'].set_position(degrees)
    sleep(0.5)
    timed_loop_motor()
    sleep(0.5)
    MOTORS['DELIVERY'].set_position(0)


def delivery(color):
    if 1 <= color <= 6:
        delivery_protocol(DELIVERY_ANGLES[color - 1])


def run():
    try:
        while not SENSORS['TOUCH'].is_pressed():
            sleep(0.1)

        deliveries_done = 0
        while deliveries_done < 6:
            move(SENSORS['LINE'].get_value()[:-1], is_forward=True)

            color = color_choosing(SENSORS['COLOR'].get_value())
            if color != 7:
                set_motor_power(0, 0)
                delivery(color)
                deliveries_done += 1

        sleep(0.5)
        MOTORS['LEFT'].set_position(-360)
        MOTORS['RIGHT'].set_position(360)
        sleep(0.5)

        while color_choosing(SENSORS['LINE'].get_value()) != 6:
            move(SENSORS['LINE'].get_value(), is_forward=False)

        MOTORS['LEFT'].set_position(-360)
        MOTORS['RIGHT'].set_position(360)

    except BaseException:
        print("Done with the program")
        set_motor_power(0, 0)
        reset_brick()
        exit()


if __name__ == "__main__":
    run()
