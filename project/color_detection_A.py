"""
Colored Cube Sorting functionality 

Ths logic is responsible for handling the detection of the color of the cube present at the bottom of the unsorted channel.

Author: Anjun Hu
January 24th, 2022
"""

from utils.brick import Motor, BP, EV3ColorSensor, TouchSensor, configure_ports, wait_ready_sensors
import time
import math as m
import argparse


def add_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file-output', type=str, required=False, default='music.log', help='Path to output file to write.')
    parser.add_argument('--ts_delay', type=float, required=False, default='0.5', help='touch sensor delay')
    parser.add_argument('--color_delay', type=float, required=False, default='0.01', help='color sensor delay')
    parser.add_argument('--batch_size', type=int, required=False, default='5', help='number of samples to take per touch sensor press')
    return parser


# MOTOR SETUP
motor_left = Motor("A")
# Set target speed first, 360 deg/sec
# Reset power limit to limitless with 0, default values:(power=0, dps=0)
motor_left.set_limits(dps=360)
# set current position to absolute pos 0deg
motor_left.reset_encoder()

# connect Port 1 to the TouchSensor and Port 2 to ColorSensor
TOUCH_SENSOR, COLOR_SENSOR = configure_ports(PORT_1=TouchSensor, PORT_2=EV3ColorSensor)

# colors
COLORS = {'R': (1.0, 0.1, 0.1),
          'G': (0.1, 1.0, 0.1), 
          'B': (0.3, 0.6, 0.7), 
          'Y': (0.8, 0.6, 0.0),}

# mapping colors to sounds
LOOKUPTABLE = {'R': 0, 'G': 120, 'B': 240}


'''
Sorting Tray Module

Based on the color determined by the color detection module at the end of the unsorted channel, 
the sorting tray will rotate by an angle associated to that respective color to drop the cube 
from the sorting tray on to the respective color channel.

Input: normalized rgb values
Output: call to set_position subroutine
'''
def color2position(r, g, b):
    print(r, g, b)
    minsqerror = 1e99
    bestfit = 'r'
    for c in COLORS.keys():
        sqerror = (r-COLORS[c][0])**2 + (g-COLORS[c][1])**2 +(b-COLORS[c][2])**2
        if sqerror < minsqerror:
            bestfit = c
            minsqerror = sqerror
    print(f'Identified Color {bestfit}')
    print(f'Moving To Position: {LOOKUPTABLE[c]}')
    motor_left.wait_is_moving()
    motor_left.set_position(LOOKUPTABLE[c])


'''
Piston Movement Module A:

The simple algorithm in this module causes the motor attached to the piston located within the unsorted channel A 
to move with just enough force to push out the cube from the unsorted channel on to the sorting tray.
'''
def piston_movement():
    # Set target speed first, 360 deg/sec
    # Reset power limit to limitless with 0, default values:(power=0, dps=0)
    motor_left.set_limits(dps=360)

    # set current position to absolute pos 0deg
    motor_left.reset_encoder()

    # TO BE TESTED #
    # move with just enough force to push out the cube from the unsorted channel on to the sorting tray
    motor_left.set_position_relative(45)

    # Optional logging    
    '''
    motor_left.wait_is_moving()
    while motor_left.is_moving():
        time.sleep(0.1)
        print("actual speed=", motor_left.get_dps(), "actual power=", motor_left.get_power(), "status=", motor_left.get_status())
    '''

'''
Request Sorting Module + Color Detection Module A

User wanting to make a sorting request will trigger a touch sensor. 
When the touch sensor is triggered,the code triggers the color sensor to start 
taking readings of the cube present at the end of the channel containing the unsorted colored cubes. 
Readings taken from color sensor are then handled by our color detection module A. 
'''
def color_movement(args):
    "Collect color sensor data."
    try:
        output_file = open(args.file_output, "w+")
        while True: # polling loop
            if TOUCH_SENSOR.is_pressed():
                start = time()
                print("Touch sensor pressed")
                print("Collect Color samples")
                r, g, b = 0, 0, 0
                for i in range(args.batch_size): # sample a batch to ensure outliers can be smoothed out by averaging
                    wait_ready_sensors() # safety measures
                    sleep(args.color_delay)
                    new_color_data = COLOR_SENSOR.get_rgb()  # RGB value[0, 255] 
                    print(new_color_data)

                    # we may encounter None here
                    try:
                        r += float(new_color_data[0])
                        g += float(new_color_data[1])
                        b += float(new_color_data[2])
                    except Exception as e:
                        print(f'Got None! {e}')
                        continue

                # normalize to account for different brightness 
                denominator = m.sqrt(r ** 2 + g ** 2 + b ** 2)

                # we may encounter zero division here
                if denominator == 0:
                    print('Got Zero Denominator!')
                    continue

                # normalize 
                r = r/denominator
                g = g/denominator
                b = b/denominator

                move = color2move(r, g, b)
                output_file.write(f"{r}, {g}, {b}\n")
                sleep(args.ts_delay) 
                print(f'Time elapsed {time()-start}')


    except Exception as e:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        print(e)
        pass

    finally:
        print("Done collecting Color samples")
        output_file.close()
        BP.reset_all() # safety measure
        exit()

if __name__ == "__main__":
    parser = add_argparser()
    args, _ = parser.parse_known_args()
    color_movement(args)
    test_motor()


