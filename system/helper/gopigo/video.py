import cv2
import numpy as np

class video:
    def __init__(self, registry):
        self.config = registry.get("config")
        self.report = registry.get("log")
        self.timer = registry.get("timer")
        print "Video Sensor      :  Start"
        self.imageFrame = None
        self.finalKey = False
        self.finalKey2 = True
        self.onlineFrame = None
        pass

    
    def whiteAndBlackImage(self,image,throshold):
        dimensional = np.array(image)
        (d1, d2) = np.shape(dimensional)
        for i in range(d1):
            for j in range(d2):
                if image[i][j] < throshold:
                    image[i][j] = 0
                else:
                    image[i][j] = 255
        return image

    def onlineVideo(self,action):
        if action == "close":
            self.finalKey = True
            return True
        cap = cv2.VideoCapture(0)
        while not self.finalKey:
            ret, self.onlineFrame = cap.read()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.finalKey = False
        cap.release()
        cv2.destroyAllWindows()

    def harris_corner_detection(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        (thresh, gray) = cv2.threshold(gray, 100,255,cv2.THRESH_BINARY)
        blackAndWhiteImage = gray
        gray = np.float32(gray)
        dst  = cv2.cornerHarris(gray, 6, 5, 0.1)
        dst  = cv2.dilate(dst, None)
        corners = len(np.unique(np.where(dst>0.1*dst.max())[0]))/6
        #image[dst>0.05*dst.max()] = [0, 0, 255]
        return corners, blackAndWhiteImage

    def destroyWindows(self):
        cv2.destroyAllWindows()

    def doEncoding(self,image,quality):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        result, encimg = cv2.imencode('.jpg', image, encode_param)
        if False == result:
            print " Encoding Error"
            self.report.error("file", "Encoding Error", "engine/static/video", True)
            quit()
        return encimg

    def doDecoding(self,image):
        decimg = cv2.imdecode(image, 1)
        return decimg

    def showImage(self, title, image):
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        pass

    def takeImage(self):
        return self.onlineFrame
