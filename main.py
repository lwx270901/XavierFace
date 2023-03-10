import random
import time
import  sys
import os
from  Adafruit_IO import  MQTTClient


import face_recognition
import cv2
import numpy as np

#Variables
image_dir = 'dataset/known'
video_capture = cv2.VideoCapture(0)

images_list  = os.listdir(image_dir)
print(images_list)
# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []
for image in images_list:
    temp = image.split(".")
    # Load a sample picture and learn how to recognize it.
    image = image_dir + '/' + image
    print(image)
    name_image = face_recognition.load_image_file(image)
    name_face_encoding = face_recognition.face_encodings(name_image)[0]
    known_face_encodings.append(name_face_encoding)
    known_face_names.append(temp[0])


face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
#End variables

#MQTT
AIO_FEED_ID = "newusers"
AIO_USERNAME = "izayazuna"
AIO_KEY = "aio_uAOd82VeiPSMHEqUZnjkfOjKez5E"
def  connected(client):
    print("Ket noi thanh cong...")
    client.subscribe(AIO_FEED_ID) 

def  subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong...")

def  disconnected(client):
    print("Ngat ket noi...")
    sys.exit (1)

def  message(client , feed_id , payload):

    print("Nhan du lieu: " + payload + "from feed id: " + feed_id)
    print("Loai du lieu: "+ str(type(payload)))
    print("retrain the model")


client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
#End Mqtt




if __name__=="__main__":

    prev_name = ""
    size_of_room = 0
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame, model="cnn")
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                name = "Unknown"
                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

                for n in face_names:
                    if name != "Unknown" and name != prev_name:
                        prev_name = name
                        
                        print("Using post method to update the event")
            
           

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


