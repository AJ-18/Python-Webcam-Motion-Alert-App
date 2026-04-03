import cv2
import time
from emailing import send_email

video = cv2.VideoCapture(0)

# Avoid black frames by giving a bit of time to load
time.sleep(1)

first_frame = None
status_list = []

while True:
    status = 0
    check, frame = video.read()

    # Transform it to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Smoothing to reduce the 'noise'
    gray_frame_gau = cv2.GaussianBlur(gray_frame,(21, 21), 0)

    # Store the first frame so it does not get overwritten on the next iteration
    if first_frame is None:
        first_frame = gray_frame_gau

    # Store the difference between the initial frame and the current frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # If a pixel has a value of 30 or more than 30, we reassign a value of 255 to that pixel
    thresh_frame = cv2.threshold(delta_frame, 35, 255, cv2.THRESH_BINARY)[1]

    # Remove the noise
    dil_frame = cv2.dilate(thresh_frame,None, iterations=2)

    # Detect contours around the white areas
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # If this is a small object (potentially fake), we just continue
        if cv2.contourArea(contour) < 5000:
            continue

        # Extract the x, y, width, and height of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Draw the rectangle around the original frame
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # If an object is detected and a rectangle is created, call the function
        if rectangle.any():
            status = 1


    status_list.append(status)

    # Update the list to include the last two items in the list
    status_list = status_list[-2:]

    # Only send the email when the object leaves the view
    if status_list[0] == 1 and status_list[1] == 0:
        send_email()

    print(status_list)

    # Display the images
    cv2.imshow("Video", frame)

    # Waits 1 ms, lets the frame render, and checks for keyboard input
    key = cv2.waitKey(1)

    # If you press 'q' the program ends
    if key == ord("q"):
        break

video.release()