import imutils,cv2
from time import sleep
from collections import defaultdict

def def_value():     return "Not Present"

color_dict=defaultdict(def_value) 
hsv_dict=defaultdict(def_value) 

def make_dict():
        color_dict[1]="Yellow"
        color_dict[2]="GreenBlue"
        color_dict[3]="Red"
        
        hsv_dict["Yellow"]=((17,116,0),(59,255,255))
        hsv_dict["GreenBlue"]=((50,112,51),(101,255,255))
        hsv_dict["Red"]=((0,141,147),(8,255,255))
        
        return maptodic()
        
def menu():
        
        img=cv2.imread("menubg.jpg") 
        
        text1="1.Yellow(Y/y)"
        text3="2.Green(G/g or B/b)"
        text2="3.Red(R/r)"
        
        cv2.putText(img,text1,(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,255),2)
        cv2.putText(img,text3,(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
        cv2.putText(img,text2,(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
        
        cv2.imshow("img",img) 
        
        while True:
                key=cv2.waitKey(1)&0xFF
                if key==ord("y") or key==ord("Y"):  return (1,(0,255,255))
                elif key==ord("G") or key==ord("g") or key==ord("B") or key==ord("b"):  return (2,(0,255,0))
                elif key==ord("R") or key==ord("r"):  return (3,(0,0,255))
                        
def maptodic():
        a=menu()
        b=a[0]
        c=a[1]        
        
        # print("a",a)
        # print("b",b)
        # print("c",c,"type",type(c))
        # print("col dict",color_dict[b])
        # print("hsv",hsv_dict[color_dict[b]])
        
        cv2.destroyAllWindows()
        return (hsv_dict[color_dict[b]],c)


def run():
        a=make_dict()
        b,e=a[0],a[1]
        colLower=b[0]
        colHigher=b[1]
        # print(colLower,colHigher)

        # url = "https://192.168.43.1:8080/video"
        # camera = cv2.VideoCapture(url)

        while True:
                (grabbed,frame)=camera.read()
                frame=imutils.resize(frame,width=600)
                blurred=cv2.GaussianBlur(frame,(11,11),0)
                hsv=cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)
                cv2.imshow("hsv",hsv)

                mask=cv2.inRange(hsv,colLower,colHigher)
                mask=cv2.erode(mask,None,iterations=2)
                mask=cv2.dilate(mask,None,iterations=2)
        
                cnts=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
                center=None
                # cv2.imshow("Frame",blurred)
        
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
                text1="Press Q or q to quit"
                text2="Press R or r choose again"
                cv2.putText(frame,text1,(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,e,2)
                cv2.putText(frame,text2,(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,e,2)
                cv2.imshow("Frame",frame)
                key=cv2.waitKey(1)&0xFF

                if key==ord("r") or key==ord("R"): 
                        cv2.destroyAllWindows()
                        a=make_dict()
                        b,e=a[0],a[1]
                        colLower=b[0]
                        colHigher=b[1]
                elif key==ord("q") or key==ord("Q"):break
        
camera=cv2.VideoCapture(0)
run()
camera.release()
cv2.destroyAllWindows()
                     
