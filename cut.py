import cv2 as cv
import numpy as np

# import serial
'''
def usart_init():          
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.5)
    if not ser.isOpen():
        print("Error::: uaset is clossed!!!")

def usart_send(xData,yData,vxData,vyData): 
    while 1:
        ser.write("PX%sY%sVX%sVY%sE" %(xData,yData,vxData,vyData,))
        if(ser.read(2) == "ok"):
            break
        else:
            print("Value is sended, but is not accepted")
'''


def get_photo():
    cap = cv.VideoCapture(0)
    if cap.isOpened():
        ret_flag, photo = cap.read()
    else:
        print("Get_photo is error!!!")
    #   cap.release()
    return photo


def binary_demo(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    binary01 = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 10)
    #   ret, binary01 = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)
    dst = cv.medianBlur(binary01, 5)
    return dst


def ROI_image(image):
    dst = binary_demo(image)
    dst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    w, h, ch = image.shape
    center_h = h // 2
    center_w = w // 2
    h_now = center_h
    w_now = center_w
    img_array = np.asarray(image)
    ROI_up, ROI_down, ROI_left, ROI_right = 1, 1, 1, 1
    while 1:
        if img_array[h_now][center_w][0] == 0:
            h_now = h_now - 1
        else:
            ROI_up = h_now
            h_now = center_w
            break
    while 1:
        if img_array[h_now][center_w][0] == 0:
            h_now = h_now + 1
        else:
            ROI_down = h_now
            h_now = center_w
            break
    while 1:
        if img_array[center_h][w_now][0] == 0:
            w_now = w_now - 1
        else:
            ROI_left = w_now
            w_now = center_h
            break
    while 1:
        if img_array[center_h][w_now][0] == 0:
            w_now = w_now + 1
        else:
            ROI_right = w_now
            w_now = center_h
            break
    # print(ROI_up,ROI_down,ROI_left,ROI_right)
    print(ROI_up, ROI_down, ROI_left, ROI_right)
    if ROI_up - ROI_down <= 0 and ROI_left - ROI_right <= 0:
        ROI = image[ROI_up + 17:ROI_down - 17, ROI_left + 17:ROI_right - 17]
        cv.imshow("ROIImage", ROI)
        print("cutted")
        return ROI_up, ROI_down, ROI_left, ROI_right
    else:
        cv.imshow("ROIImage", image)
        print("nope")
        return 0, w, 0, h


def ball_Pos(roi_up, roi_down, roi_left, roi_right):
    capture = cv.VideoCapture(0)
    Cut02 = 18
    last_cx = 0
    last_cy = 0
    while (True):
        ret, frame = capture.read()
        if ret == False:
            break
        cv.imshow("frame", frame)
        ROI = frame[roi_up + Cut02:roi_down - Cut02, roi_left + Cut02:roi_right - Cut02]
        dst = binary_demo(ROI)
        cv.imshow("ROI_Image", dst)
        h, w, ch = frame.shape
        result = np.zeros((h, w, ch), dtype=np.uint8)
        contours, hireachy = cv.findContours(dst, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for cnt in range(len(contours)):
            mm = cv.moments(contours[cnt])
            try:
                cx = int(mm['m10'] / mm['m00'])
                cy = int(mm['m01'] / mm['m00'])
                cv.circle(result, (cx, cy), 3, (0, 0, 255), -1)
                vx = (cx - last_cx) / 50
                vy = (cy - last_cy) / 50
                last_cx = cx
                last_cy = cy
                #                usart_send(cx,cy,vx,vy)
                cv.imshow("POINT_POS", result)
            except:
                pass
        c = cv.waitKey(50)
        if c == 27:
            break


if __name__ == "__main__":
    print("-----------------Hello ball--------------")
    # src = cv.imread("D:/123.jpg")
    src = get_photo()
    baseImage = get_photo()
    cv.imshow("baseImage", baseImage)
    roi_up, roi_down, roi_left, roi_right = ROI_image(src)
    ball_Pos(roi_up, roi_down, roi_left, roi_right)
    cv.waitKey(0)
    cv.destroyALLWindows()
