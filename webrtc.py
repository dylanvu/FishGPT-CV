import cv2

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()  # return a single frame in variable `frame`
    # frame = cv2.resize(frame, (1920, 1080))
    cv2.imshow('Capturing Video', frame)  # display the captured image
    key = cv2.waitKey(1) & 0xFF
    if key == ord('y'):  # exit on pressing 'y'
        cv2.destroyAllWindows()
        break

cap.release()
