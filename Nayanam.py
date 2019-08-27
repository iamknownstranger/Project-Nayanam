import cv2
import subprocess, sys
import time
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
cap = cv2.VideoCapture(0)
powershell = subprocess.Popen(['powershell.exe', 'Get-Ciminstance -Namespace root/WMI -ClassName WmiMonitorBrightness'], stdout=subprocess.PIPE, shell=True)
print(powershell)
current_brightness = 100
while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    counter = 0
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,127,255),2)
            if True:
                current_brightness = current_brightness//2
                p = subprocess.Popen(['powershell.exe',
                                  '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,'+str(current_brightness)+')'], stdout=subprocess.PIPE, shell=True)
                #I can add path to the hot key to get whenever the process need to be done so that the scrpt will continue to run in the background as well as the command prompt window will not be poped uo every single time
                time.sleep(3600)
    else:
        counter += 1
        time.sleep(5)
        if(counter == 1):
            process = subprocess.Popen("powershell.exe (Add-Type '[DllImport(\"user32.dll\")]^public static extern int SendMessage(int hWnd, int hMsg, int wParam, int lParam);' -Name a -Pas)::SendMessage(-1,0x0112,0xF170,2)")


    cv2.imshow('See Yourself Buddy',img)    
    key = cv2.waitKey(30) & 0xff
    #ESC key to close the window and terminate the program
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
