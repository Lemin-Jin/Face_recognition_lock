import cv2
import os,glob
import face_recognition
import time
import requests
import argparse
import logging
import concurrent.futures as future 


def converge(value):
    if int(value) >= 0 and int(value) < 10:
        return int(value)
    else:
        raise argparse.ArgumentTypeError("wrong scaling factor")
parser = argparse.ArgumentParser(description="face detection lock")
parser.add_argument('-s', dest="scale", action="store", default=2, \
                    help='''image scaling ratio, for example, 
                    0 is not scaling, 1 is processing the image with half length and width''',\
                        type=converge)
parser.add_argument('-d', dest="display", action="store_true", default=False,\
                    help="to display the camera image")
# parser.add_argument("-hook", dest="webhook_id", action="store", required=True, \
#                     help="webhook id for home assistant webhook trigger")
parser.add_argument('-url', dest="url", action="store", required=True, \
                    help="url for home assistant")
parser.add_argument('-debug',dest="debug",action="store_true", default=False, \
                    help="turn on debug logging")
parser.add_argument('-n', dest="names", action="store", required=True, nargs="*", \
                    help="names to unlock faces")
args = parser.parse_args()

globals().update(vars(args))

if debug is True:
    logging.basicConfig(level=10)
else:
    logging.basicConfig(level=30)

webhook_url = url
shrink_factor = 1 / (1 << scale)
restore_factor = 1 << scale
os.chdir(os.getcwd() + "/faces")

known_encodings = {}
[known_encodings.setdefault(name, []) for name in names]
logging.debug("loading and encoding image")
start_encoding = time.time()

counter = 0

for file_name in names:
    curfile = file_name + "?.jpg"
    files = glob.glob(curfile)
    if(len(files) == 0):
        logging.warning("image of " + file_name + \
                        " does not exist in " + os.getcwd() +", please check image name format")
        counter += 1
        continue

    with future.ProcessPoolExecutor() as executor:
        faces = []

        loaded_images = executor.map(face_recognition.load_image_file, files)

        for face in loaded_images:
            faces.append(face)
        
        encodings = executor.map(face_recognition.face_encodings, faces)

        for encoding in encodings:
            if len(encoding) != 0:
                known_encodings[file_name].append(encoding[0])
        
    # for file in files:
    #     known_face = face_recognition.load_image_file(file)
    #     var =  face_recognition.face_encodings(known_face)
    #     #logging.debug("currently load files: "+file)
    #     if len(var) != 0:
    #         knonw_face_encoding = var[0]
    #         known_encodings[file_name].append(knonw_face_encoding)

if counter == len(names):
    logging.error("no images in folder matches names, exitting")
    exit()

logging.debug("encoding time is: " + str(time.time() - start_encoding))
logging.debug("file encoding complete")
face_locations = []
face_encodings = []
face_names = []

verification_counter = {}
[verification_counter.setdefault(name, [0, time.time()]) for name in names]


cap = cv2.VideoCapture(0)

to_process = True
while True:
    ret, frame = cap.read()
    if to_process == True:
        small_frame = cv2.resize(frame, (0,0), fx = shrink_factor, fy = shrink_factor)
        face_locations = face_recognition.face_locations(small_frame)
   
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_names = []
        # loop through every face dectected in the frame
        for face_encoding in face_encodings:
            #loop through all the known names

            for key in known_encodings.keys():
                if(len(known_encodings[key]) == 0):
                    continue
                matches = face_recognition.compare_faces(known_encodings[key], face_encoding, tolerance= 0.4)
                count = 0
                for item in matches:
                    if item == True:
                        count = count + 1
                if count/len(matches)  > 0.7:
                    logging.debug(key + "is captured")
                    face_names.append(key)
                    verification_counter[key][0] += 1

                
                if verification_counter[key][0] >= 5:
                    if time.time() - verification_counter[key][1] > 30: 
                        logging.debug("requst send")
                        r = requests.post(webhook_url)
                        verification_counter[key][1] = time.time()
                        verification_counter[key][0] = 0
            
        
        if display is True:
            for (top, right, bottom, left), name in zip(face_locations, face_names):

                top *= restore_factor
                right *= restore_factor
                bottom *= restore_factor
                left *= restore_factor
                
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    if display is True:
        cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    to_process = not to_process

cap.release()
cv2.destroyAllWindows()





