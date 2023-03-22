# import the opencv library
import cv2
import numpy as np
from datetime import datetime
  

class Bolean:
    def __init__(self):
        self.value = True 

class Frame:
    def __init__(self):
        self.value = np.zeros((100,100),np.uint8)

def voidNone ():
    pass
class ClickIcon:
    def __init__(self,path,pos=(0,0),size= (20,20),callback=voidNone):
        self.path = path
        self.img = cv2.resize(cv2.imread(path),size)
        self.pos = np.array(pos)
        self.size = np.array(size)
        self.callback = callback 
    def set_click_callback(self,callback):
        self.callback = callback
    def check_click (self,click_pos):
        if click_pos[0] > self.pos[0] + self.size[0]:return False
        if click_pos[1] > self.pos[1] + self.size[1]:return False
        if click_pos[0] < self.pos[0]:return False
        if click_pos[1] < self.pos[1]:return False
        return True


  
def composeIcons(img,icons:[ClickIcon]):
    img = img.copy()
    for icon in icons:
        img[icon.pos[0]:icon.pos[0]+icon.size[0],icon.pos[1]:icon.pos[1]+icon.size[1]] = icon.img 
    return img


# define a video capture object
vid = cv2.VideoCapture(2)

loop_cond = Bolean()
def end_loop():loop_cond.value= False

frame_to_save = Frame()
def save_frame():
    current_time= datetime.now()
    time_str = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    cv2.imwrite(f"./capture/{time_str}.png",frame_to_save.value)
icons = [ClickIcon("./icons/camIcon.png",(0,0),(50,50),save_frame),ClickIcon("./icons/closeIcon.png",(0,590),(50,50),end_loop)]



def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        for icon in icons:
            if icon.check_click((y,x)):
                icon.callback()
          

while(loop_cond.value):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    if not ret: continue
    frame_to_save.value = frame.copy()
    frame = composeIcons(frame, icons)

  
    # Display the resulting frame
    cv2.imshow('frame', frame)
    cv2.setMouseCallback('frame', mouse_click)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
