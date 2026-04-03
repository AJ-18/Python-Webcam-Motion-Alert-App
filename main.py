import cv2
import time

video = cv2.VideoCapture(0)

# Avoid black frames by giving a bit of time to load
time.sleep(1)

first_frame = None

while True:
    check, frame = video.read()

    # Transform it to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Smoothing to reduce the 'noise'
    gray_frame_gau = cv2.GaussianBlur(gray_frame,(21, 21), 0)

    # Display the images
    cv2.imshow("My video", gray_frame_gau)

    # Store the first frame so it does not get overwritten on the next iteration
    if first_frame is None:
        first_frame = gray_frame_gau

    #
    key = cv2.waitKey(1)

    # If you press 'q' the program ends
    if key == ord("q"):
        break

video.release()