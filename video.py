import face_recognition
import cv2
import csv

import time

# This is a demo of running face recognition on a video file and saving the results to a new video file.
#
# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

start = time.time()

# Open the input movie file
input_movie = cv2.VideoCapture("video.mp4")
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

# Create an output movie file (make sure resolution/frame rate matches input video!)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_movie = cv2.VideoWriter('output.avi', fourcc, 29.97, (640, 360))

# Load some sample pictures and learn how to recognize them.
lmm_image = face_recognition.load_image_file("tom.jpg")
lmm_face_encoding = face_recognition.face_encodings(lmm_image)[0]

# al_image = face_recognition.load_image_file("alex-lacamoire.png")
# al_face_encoding = face_recognition.face_encodings(al_image)[0]

known_faces = [
    lmm_face_encoding,
    # al_face_encoding
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
frame_number = 0

path = 'output.csv'

def isThresholdPassed(count,threshold):
    if count < threshold:
        return False
    else:
        return True

#eg: index == 99, FPS == 100, nearestSecond => 0th
#eg:index == 100, FPS == 100, nearestSecond => 1st
def indexToNearestSecond(index, FPS):
    if isinstance(index, int) and isinstance(FPS, int):
        return index // FPS #integer quotient

#input: int second, int value (1 or 0), path to output
#outputs [SECOND, VALUE] to path as csv row
def outputResultToCSV(second, value, path):
    with open(path, mode = 'a+', newline='') as my_csv:
            my_csv_writer = csv.writer(my_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            my_csv_writer.writerow([second, value])

THRESHOLD = 1
positive_detection = False #this represents main out value. Should it just be int?
detection_count = 0
FPS = 30

while True:
    # Grab a single frame of video
    ret, frame = input_movie.read()
    frame_number += 1

    if frame_number <= 2000: continue
    if frame_number >= 3000: break

    #TODO:replace this with threshold code, or combine threshold with larger modulus
    if frame_number % 5 != 0: continue

    # Quit when the input video file ends
    if not ret:
        break

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video


    # start = time.time()
    face_locations = face_recognition.face_locations(rgb_frame)
    # end = time.time()
    # print('Detection took {}s'.format(end - start))

    # start = time.time()
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    # end = time.time()
    # print('Extraction took {}s'.format(end - start))

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        # start = time.time()
        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.60)
        # end = time.time()
        # print('Comparison took {}s'.format(end - start))

        # If you had more than 2 faces, you could make this logic a lot prettier
        # but I kept it simple for the demo
        name = None
        if match[0]:
            name = "Tom Cruise"
        # elif match[1]:
            # name = "Alex Lacamoire"

        face_names.append(name)

    # Label the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if not name:
            continue

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Write the resulting image to the output video file
    print("frame {} / {} processed".format(frame_number, length))
    output_movie.write(frame)
    # cv2.imshow('Video', frame)

    positiveDetection = isThresholdPassed(detection_count, THRESHOLD)
    
    #We have some threshold for positive detection, eg: six images in a second
    if positiveDetection == True:

        #write output to file
        outputResultToCSV(indexToNearestSecond(frame_number, FPS), 1, path)   #csv row == [SECOND, INT_VALUE]
        
        #jump index to start of next second
        frame_offset = FPS - (frame_number % FPS)
        frame_number += frame_offset  #0-> FPS, FPS-1 -> FPS
        continue
    #else keep searching this second or advance to next

    
    if frame_number % FPS == 0 or (frame_number % FPS > FPS /2):  #FPS == 30, 29 -> 29, 30 -> 0

        #write output to file
        outputResultToCSV(indexToNearestSecond(frame_number, FPS), 0, path)  #csv row == [SECOND, INT_VALUE]
        #jump to next second
        continue

    # Hit 'q' on the keyboard to quit!
    # if cv2.waitKey(1) & 0xFF == ord('q'):
        # break

# All done!
input_movie.release()
cv2.destroyAllWindows()

end = time.time()
print('Processing took {}s'.format(end - start))
