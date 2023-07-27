import recorder
import argparse
import os

path = os.getcwd() + "/faces"

def arg_range(value):
    if int(value) > 0 and int(value) < 100:
        return int(value)
    else:
        raise argparse.ArgumentTypeError("wrong scaling factor")
parser = argparse.ArgumentParser(description="face detection lock")
parser.add_argument('-num', dest="num_pics", action="store", default=1, \
                    help="num of image stored per person",\
                        type=arg_range)
parser.add_argument('-t', dest="time_out", action="store", default=100, \
                    help="time before capture time out",\
                        type=arg_range)
parser.add_argument('-d', dest="display", action="store_true", default=False,\
                    help="to display the camera image")
parser.add_argument('-n', dest="names", action="store", required=True, nargs="*", \
                    help="names to unlock faces")

args = parser.parse_args()

globals().update(vars(args))

profiles = []

for name in names:
    profiles.append(recorder.profile(name, num_pics, path, display, time_out))

def scan_input():
    key = input()
    while True:
        if key == "c":
            return True
        elif key == 'q':
            return False
        else:
            print("invalid input, re-enter please")
            key = input()
        

for cur_profile in profiles:
    print("storing image for " + cur_profile.name)
    print("press c to continue, or press q to exit")
    if scan_input() is False:
        break
    result = cur_profile.store_img()
    if result is True:
        print("image store success")
    else:
        print("image store time out")
        
print("recording is over")