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
motor_rotate_b = Motor("B")
motor_rotate_c = Motor("C")
motor_push = Motor("D")
# Set target speed first, 360 deg/sec
# Reset power limit to limitless with 0, default values:(power=0, dps=0)
motor_rotate_b.set_limits(dps=1500)
motor_rotate_c.set_limits(dps=1500)
motor_push.set_limits(dps=500)
# set current position to absolute pos 0 deg
#motor_rotate_b.set_position(0)
#motor_rotate_c.set_position(0)
motor_push.set_position(0)
motor_rotate_b.reset_encoder()
motor_rotate_c.reset_encoder()
motor_push.reset_encoder()
# connect Port 1 to the TouchSensor and Port 2 to ColorSensor
TOUCH_SENSOR_SORT, COLOR_SENSOR_SORT = configure_ports(PORT_1=TouchSensor, PORT_2=EV3ColorSensor)
# Works with motor_push.set_position(0)
PISTON_ANGLE = [-90,  -130,  -180,  -250, -280, -360]

# colorss
COLORS = {'R': (1.0, 0.1, 0.1),
          'G': (0.1, 1.0, 0.1), 
          'B': (0.3, 0.6, 0.7), 
          'Y': (0.8, 0.6, 0.0),}

# mapping colors to sounds
LOOKUPTABLE_B = {'R': 0, 'G': 60, 'B': -50}
LOOKUPTABLE_C = {'R': 0, 'G': -60, 'B': 50}

'''
Sorting Tray Module

Based on the color determined by the color detection module at the end of the unsorted channel, 
the sorting tray will rotate by an angle associated to that respective color to drop the cube 
from the sorting tray on to the respective color channel.

Input: normalized rgb values
Output: call to set_position subroutine
'''
def color2position(r, g, b, cubenumber):
    print(r, g, b)
    minsqerror = 1e99
    bestfit = 'R'
    for c in COLORS.keys():
        sqerror = (r-COLORS[c][0])**2 + (g-COLORS[c][1])**2 +(b-COLORS[c][2])**2
        if sqerror < minsqerror:
            bestfit = c
            minsqerror = sqerror

    print(f'Identified Color {bestfit}')
    print(f'Moving To Position: {LOOKUPTABLE_C[bestfit]}')
    motor_rotate_c.set_position(LOOKUPTABLE_C[bestfit])
    motor_rotate_b.set_position(LOOKUPTABLE_B[bestfit])
    time.sleep(2)
    motor_push.set_position_relative(PISTON_ANGLE[cubenumber])
    time.sleep(2)
    motor_rotate_b.set_position(0)
    motor_rotate_c.set_position(0)
    motor_push.set_position(0)

'''
Request Sorting Module + Color Detection Module A

User wanting to make a sorting request will trigger a touch sensor. 
When the touch sensor is triggered,the code triggers the color sensor to start 
taking readings of the cube present at the end of the channel containing the unsorted colored cubes. 
Readings taken from color sensor are then handled by our color detection module A. 
'''
def color_movement(args):
    cubenumber = 0
    "Collect color sensor data."
    try:
        output_file = open(args.file_output, "w+")
        while True: # polling loop
            if TOUCH_SENSOR_SORT.is_pressed():
                start = time.time()
                print("Touch sensor pressed")
                print("Collect Color samples")
                r, g, b = 0, 0, 0
                for i in range(9): # sample a batch to ensure outliers can be smoothed out by averaging
                        wait_ready_sensors() # safety measures
                        time.sleep(0.1)
                        new_color_data = COLOR_SENSOR_SORT.get_rgb()  # RGB value[0, 255] 
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

                move = color2position(r, g, b, min(len(PISTON_ANGLE),cubenumber))
                
                output_file.write(f"{r}, {g}, {b}\n")
                time.sleep(1) 
                print(f'Time elapsed {time.time()-start}')


    except Exception as e:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
            print(e)
            pass

    finally:
            print("Done collecting Color samples")
            output_file.close()
                    

def test_motor(pos):
    
    for i in range(pos):
        print("turning")
        motor_bottom.set_position(i)
        time.sleep(.1)


if __name__ == "__main__":
    parser = add_argparser()
    args, _ = parser.parse_known_args()
    color_movement(args)
       
    
    
    
    
    



