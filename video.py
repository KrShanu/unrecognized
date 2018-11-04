import face_recognition
import cv2
import csv
import sys
import time

# For benchmarks
start = time.time()

# Open the input movie file
movie_filename = 'video.mp4'
input_movie = cv2.VideoCapture(movie_filename)
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

# configure output file
path = 'output.csv'

# Find fps of the clip
fps = round(input_movie.get(cv2.CAP_PROP_FPS))
print('{} @ {} fps'.format(movie_filename, fps))

# Create an output movie file (make sure resolution/frame rate matches input video!)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_movie = cv2.VideoWriter('output.avi', fourcc, fps, (640, 360))

# Load some sample pictures and learn how to recognize them.
lmm_image = face_recognition.load_image_file("image.jpg")
lmm_face_encoding = face_recognition.face_encodings(lmm_image)[0]

known_faces = [
    lmm_face_encoding
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
frame_number = 0

length_in_seconds = (length // fps ) + 1
if length % fps == 0:
    length_in_seconds -= 1

is_tom_there = [0] * length_in_seconds
current_second = 0;


THRESHOLD = 1
positive_detection = False #this represents main out value. Should it just be int?
detection_count = 0
frame_offset = 0

i_see_you = False

while True:

    while frame_offset!=0:
        print("frame {} / {} processed, offset {}".format(frame_number, length, frame_offset))
        ret, frame = input_movie.read()
        output_movie.write(frame)
        cv2.imshow('Video', frame)
        frame_offset -= 1
        frame_number += 1

    # Grab a single frame of video
    ret, frame = input_movie.read()
    frame_number += 1

    # Debug
    # if frame_number <= 890: continue
    # if frame_number >= 3000: break
    # if frame_number % 5 != 0: continue

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
            name = "Wanted"
            i_see_you = True
            detection_count += 1
            print("Scientology")
        # elif match[1]:
            # name = "Alex Lacamoire"

        face_names.append(name)

    # Label the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        if not name:
            continue

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Write the resulting image to the output video file
    print("frame {} / {} processed, count {}".format(frame_number, length, detection_count))
    output_movie.write(frame)
    cv2.imshow('Video', frame)

    if i_see_you:
        current_second = frame_number // fps
        is_tom_there[current_second] = 1

        frame_offset = fps - (frame_number % fps)
        # frame_number += frame_offset  #0-> fps, fps-1 -> fps
        # cvSetCaptureProperty(capture, CV_CAP_PROP_POS_FRAMES, frameIndex);

        i_see_you = False

    if frame_number >= length:
        break

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

with open(path, mode = 'w+', newline='') as my_csv:
    for i in range(0, length_in_seconds):
        my_csv_writer = csv.writer(my_csv, quoting=csv.QUOTE_MINIMAL)
        my_csv_writer.writerow([i, is_tom_there[i]])

# All done!
input_movie.release()
cv2.destroyAllWindows()

end = time.time()
print('Processing took {}s'.format(end - start))
