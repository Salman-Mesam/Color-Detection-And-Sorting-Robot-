"""
Colored Cube Retrieval Functionality

Logic responsible for delivering the requested colored cube to the delivery area.

Author: Anjun Hu
Match 15th, 2022
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


motor_left = Motor("A")

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
Originally writtend by Ryan Au
Retained for morot component testing purposes
'''
def test_motor():
    # Set target speed first, 360 deg/sec
    # Reset power limit to limitless with 0, default values:(power=0, dps=0)
    motor_left.set_limits(dps=360)

    # set current position to absolute pos 0deg
    motor_left.reset_encoder()

    # command to move to absolute pos 270deg
    motor_left.set_position(270)
    print("motor_left.set_position(270)")
    input("# Press any key to continue...")

    # command to rotate 90deg away from current position
    motor_left.set_position_relative(90)
    print("motor_left.set_position_relative(90)")
    input("Press any key to continue...")

    """Tests 3 different speeds. set_dps overrides set_limits.
    dps=180, rotation_dist=720
    dps=360, rotation_dist=1080
    dps=540, rotation_dist=1440
    """
    for i, speed in enumerate([180, 360, 180*3]):
        motor_left.set_dps(speed) # overrides previous limits. Use limits or set_dps
        motor_left.set_position_relative(360 * (i+2))
        motor_left.wait_is_moving()
        while motor_left.is_moving():
            time.sleep(0.1)
            print("actual speed=", motor_left.get_dps(), "actual power=", motor_left.get_power(), "status=", motor_left.get_status())


'''
Piston Triggering Module B + Color Detection Module B

Takes normalized mean values for the RGB readings to decide which color was read in by the color sensor

The angular position corresponds to the position of the intended piston within the target color channel 
'''
def piston_movement_sortedChannel(r, g, b):
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
    motor_left.set_position(LOOKUPTABLE[c])



'''
Request Processing Module + Color Detection Module B

a polling loop that checks for when the touch sensor is pressed by user (when a retrieval request is made
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

                move = piston_movement_sortedChannel(r, g, b) # record the music!
                output_file.write(f"{r}, {g}, {b} --> {sound}\n")
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


