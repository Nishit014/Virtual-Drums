import cv2
import numpy as np
#import matplotlib.pyplot as plt
from pygame import mixer

def plays(sound):
    if sound==1:
        drum_hat.play()
    if sound==2:
        drum_snare.play()
    if sound==3:
        drum_hat1.play()
    if sound==4:
        drum_snare1.play()

def detect_area(frame,sound):

    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,greenl,greenu)
    detected=np.sum(mask)
    #print(detected)
    if detected>250000:
        plays(sound)
    return mask

mixer.init()
drum_snare=mixer.Sound('./drums/snare_1.wav')
drum_hat=mixer.Sound('./drums/high_hat_1.ogg')
drum_snare1=mixer.Sound('./drums/snare_2.wav')
drum_hat1=mixer.Sound('./drums/high_hat_2.wav')

cap=cv2.VideoCapture(0)
d1=cv2.resize(cv2.imread('./drums/df.jpeg'),(0,0),fx=0.5,fy=0.2)

greenl=(25,52,72)
greenu=(102,255,255)

while True:
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)

    #cv2.rectangle(frame,(270,432),(465,500),(255,0,0),1)#h1
    #cv2.rectangle(frame,(830,432),(1030,500),(255,0,0),1)#h2
    #cv2.rectangle(frame,(940,520),(1130,570),(255,0,0),1)#h3
    #cv2.rectangle(frame,(470,462),(640,570),(255,0,0),1)#s1
    #cv2.rectangle(frame,(700,462),(825,570),(255,0,0),1)#s2
    #cv2.rectangle(frame,(350,530),(550,630),(255,0,0),1)#s3
    #cv2.rectangle(frame,(820,550),(960,610),(255,0,0),1)#s4

    h1=frame[430:501,269:470]
    mask1=detect_area(h1,1)
    h2=frame[430:505,829:1030]
    mask2=detect_area(h2,1)
    h3=frame[520:560,960:1130]
    mask3=detect_area(h3,3)
    s1=frame[470:570,470:650]
    mask4=detect_area(s1,2)
    s2=frame[480:580,700:830]
    mask5=detect_area(s2,2)
    s3=frame[530:620,350:520]
    mask6=detect_area(s3,4)
    s4=frame[550:600,829:959]
    mask7=detect_area(s4,4)

    rows,col,channels=d1.shape
    roi=frame[432:rows+432,0:col]

    gray=cv2.cvtColor(d1,cv2.COLOR_BGR2GRAY)
    ret,maskp=cv2.threshold(gray,240,255,cv2.THRESH_BINARY_INV)
    maskp_inv=cv2.bitwise_not(maskp)

    frame_bg=cv2.bitwise_and(roi,roi,maskp_inv)
    d1_fg=cv2.bitwise_and(d1,d1,mask=maskp)

    dframe=cv2.add(frame_bg,d1_fg)
    frame[432:rows+432,0:col]=dframe

    font=cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame,'Virtual Drums',(0,30),font,1,(0,0,0),2,cv2.LINE_AA)
    cv2.putText(frame,'Created by Nishit Mehrotra',(840,715),font,1,(0,0,0),2,cv2.LINE_AA)

    cv2.imshow('frame',frame)
    #cv2.imshow('d1',d1)
    #cv2.imshow('dframe',dframe)
    #cv2.imshow('frame1',s2)
    #cv2.imshow('mask',mask6)

    if cv2.waitKey(1)==27:
        break
cap.release()
cv2.destroyAllWindows()
