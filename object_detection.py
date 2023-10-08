import imutils,cv2
from time import sleep
def menu():
        
        choice=2
        img=cv2.imread("menubg.jpg") 
        
        text1="1.Yellow"
        text2="2.Red"
        text3="3.Greeen"
        cv2.putText(img,text1,(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)
        cv2.putText(img,text3,(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),2)
        cv2.putText(img,text2,(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),2)
        cv2.imshow("img",img) 
        while True:
                key=cv2.waitKey(1)&0xFF
                if key==ord("y") or key==ord("Y"):  
                        choice=1
                        break
        print("choice",choice)
        return choice 

def maptodic():
        a=0
        a=menu()
        color_dict=dict()
        hsv_dict=dict()
        color_dict[1]="Yellow"
        hsv_dict["Yellow"]=((17,116,0),(59,255,255))
        return hsv_dict[color_dict[a]]

b=maptodic()
colLower=b[0]
colHigher=b[1]
# cv2.waitKey(0)
cv2.destroyAllWindows()
print(colLower,colHigher)
camera=cv2.VideoCapture(0)
# url = "https://192.168.43.1:8080/video"
# camera = cv2.VideoCapture(url)
while True:
        (grabbed,frame)=camera.read()
        frame=imutils.resize(frame,width=600)
        blurred=cv2.GaussianBlur(frame,(11,11),0)
        hsv=cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)
        # cv2.imshow("hsv",hsv)
        mask=cv2.inRange(hsv,colLower,colHigher)
        mask=cv2.erode(mask,None,iterations=2)
        mask=cv2.dilate(mask,None,iterations=2)
        cnts=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center=None
        if len(cnts)>0:
                c=max(cnts,key=cv2.contourArea)
                ((x,y),radius)=cv2.minEnclosingCircle(c)
                M=cv2.moments(c)
                center=(int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
                if radius>10:
                        cv2.circle(frame,(int(x),int(y)),int(radius),(0,255,255))
                        cv2.circle(frame,center,5,(0,255,0),-1)
                        if(center[0]<150):print("Left")
                        elif(center[0]>450):print("Right")
                        elif(radius<250):print("Front")
                        else:print("Stop")
                cv2.imshow("Frame",frame)
                key=cv2.waitKey(1)&0xFF
                if key==ord('Q') or key==ord('q'):break
camera.release()
cv2.destroyAllWindows()
                 
        