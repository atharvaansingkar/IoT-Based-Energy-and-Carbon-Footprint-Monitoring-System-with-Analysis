import cv2
from PIL import Image
import numpy as np

"""
 7 segments indexes are:
 0: top,
 1: top left,
 2: top right,
 3: middle,
 4: bottom left,
 5: bottom right,
 6: bottom
"""
segments = {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (1, 0, 1, 1, 1, 0, 1): 2,
    (1, 0, 1, 1, 0, 1, 1): 3,
    (0, 1, 1, 1, 0, 1, 0): 4,
    (1, 1, 0, 1, 0, 1, 1): 5,
    (1, 1, 0, 1, 1, 1, 1): 6,
    (1, 0, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9
}

def cv2_2_pil(cv2img, transform=cv2.COLOR_BGR2RGB):
    return Image.fromarray(cv2.cvtColor(cv2img, transform))

def get_digit(img, segment_pos):
    active = map(lambda x: int(np.count_nonzero(get_dig_sub(img, x[0], x[1], 4, 4)) > 8), segment_pos)
    return segments.get(tuple(active), 'x')

def get_dig_sub(img, x, y, width, height):
    return img[y:y + height, x:x + width]

def extract_and_identify_digit(img, x, y, width, height, segment_pos):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, imthresh = cv2.threshold(imgray, 76, 255, cv2.THRESH_BINARY_INV)
    imthresh = cv2.dilate(imthresh, np.ones((2, 2), np.uint8), iterations=5)
    digit_area = get_dig_sub(imthresh, x, y, width, height)
    digit = get_digit(digit_area, segment_pos)

    cv2.imshow("Digit Area", digit_area)
    cv2.imwrite(f"Digit_Area_{x}_{y}.png", digit_area)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()
    return digit

def capture_image_from_webcam(save_path='captured_image.png'):
    cap = cv2.VideoCapture(0)  

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return None

    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame from webcam.")
        return None

    cap.release()
    cv2.imwrite(save_path, frame)  
    return frame

if __name__ == "__main__":
    image = capture_image_from_webcam()

    if image is None:
        print("Error: No image captured from webcam.")
    else:
        digit_parameters = [
            # (x, y, width, height, segment_pos)
            (0, 227, 96, 186, [(58, 15), (17, 53), (89, 54), (48, 95), (10, 132), (78, 138), (38, 174)]),      # first digit
            (100, 227, 100, 186, [(61, 16), (22, 59), (94, 67), (54, 98), (13, 143), (86, 147), (44, 178)]),  # second digit
            (212, 230, 100, 186, [(40, 9), (16, 38), (81, 53), (45, 87), (8, 119), (70, 142), (42, 171)]),     # third digit
            (325, 285, 79, 135, [(44, 19), (6, 45), (65, 50), (34, 73), (8, 108), (62, 107), (31, 127)]),     # fourth digit
        ]

        identified_digits = []
        for (x, y, width, height, segment_pos) in digit_parameters:
            identified_digit = extract_and_identify_digit(image, x, y, width, height, segment_pos)
            identified_digits.append(str(identified_digit))
        
        result_string = ''.join(identified_digits[:3]) + '.' + identified_digits[3] + ' KWh'
        
        consumption_value = float(result_string.split()[0])

        carbon_footprint = consumption_value * 0.85


        #carbon footprint
        print('\n#############################################################\n')
        print("Current Consumption:", result_string)
        print("Carbon Footprint:", carbon_footprint, "kg CO2e   (at 0.85 emission factor)")
        if carbon_footprint < 7085:
         print('Remark: Consumption is low compared to global average\nGood Work!')
        else:
            print('You need to reduce your consumption')
        print('\n#############################################################\n')