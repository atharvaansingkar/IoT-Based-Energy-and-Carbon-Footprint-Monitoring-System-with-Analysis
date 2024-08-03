import cv2

def main():
    # Open the default camera (usually the first camera indexed as 0)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return

    # Initialize a counter for saved images
    img_counter = 0

    # Loop to continuously capture frames from the camera
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame was captured successfully
        if not ret:
            print("Error: Unable to capture frame.")
            break

        # Display the captured frame
        cv2.imshow('Webcam', frame)

        # Check for key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            # Save the current frame as an image file
            img_name = f"captured_frame_{img_counter}.png"
            cv2.imwrite(img_name, frame)
            print(f"Frame captured and saved as {img_name}")
            img_counter += 1

    # Release the camera and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()