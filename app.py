from flask import Flask, render_template, Response
import cv2 as cv
import mediapipe as mp
import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



def gen_frames():
    camera = cv.VideoCapture(0)
    pTime=0

    mpFaceDetection = mp.solutions.face_detection
    mpDraw = mp.solutions.drawing_utils
    faceDetection = mpFaceDetection.FaceDetection(0.75)
    while True:
        success, frame = camera.read() 
        if not success:
            break
        else:
            imgRGB = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
            results = faceDetection.process(imgRGB)
            if results.detections:
                for id,detection in enumerate(results.detections):
                    bboxC = detection.location_data.relative_bounding_box
                    ih,iw,ic = frame.shape
                    bbox = int(bboxC.xmin * iw),int(bboxC.ymin * ih),int(bboxC.width * iw),int(bboxC.height * ih)        
                    frame = createFrame(frame,bbox)
                    cv.putText(frame,f'FA: {int(detection.score[0]*100)}%',(bbox[0],bbox[1] - 20),cv.FONT_HERSHEY_PLAIN,2,(255,0,255),2)
                
                localtime = time.ctime()
                
                # cv.imwrite(filename=localtime, img=frame)
                
                    
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            # lt = localtime.replace(" ", "")

            cv.putText(frame,f'FPS: {int(fps)}',(10,50),cv.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
            cv.putText(frame,f'{localtime}',(300,470),cv.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),1)
            
            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
def createFrame(frame,bbox,l=20,s=5):
    x,y,w,h =bbox
    x1,y1 = x+w,y+h
    cv.rectangle(frame,bbox,(255,0,255),2)
    cv.line(frame,(x,y),(x+l,y),(255,0,255),s)
    cv.line(frame,(x,y),(x,y+l),(255,0,255),s)
    # top right
    cv.line(frame,(x1,y),(x1-l,y),(255,0,255),s)
    cv.line(frame,(x1,y),(x1,y+l),(255,0,255),s)
    # bottom left
    cv.line(frame,(x,y1),(x+l,y1),(255,0,255),s)
    cv.line(frame,(x,y1),(x,y1-l),(255,0,255),s)
    # bottom right
    cv.line(frame,(x1,y1),(x1-l,y1),(255,0,255),s)
    cv.line(frame,(x1,y1),(x1,y1-l),(255,0,255),s)
        
    return frame

if __name__ == "__main__":
    app.run(debug=True)