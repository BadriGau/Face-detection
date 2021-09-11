from itertools import chain
from flask import Flask, render_template, Response,flash,session,redirect,url_for
import cv2 as cv
import mediapipe as mp
import time
import os
from forms import LoginForm,AddPersonForm
from config import Config
from werkzeug import secure_filename
app=Flask(__name__)
app.config.from_object(Config)


@app.route('/index')
def index():
    if not session.get('username'):
        return redirect(url_for('login'))
    if not os.path.exists('Breach'):
        os.mkdir("Breach")
    return render_template('stream.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')




def gen_frames():
    camera = cv.VideoCapture(0) #second parameter cv.CAP_DSHOW or CAP_MSMF
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
                    cv.putText(frame,f'Detection%: {int(detection.score[0]*100)}%',(bbox[0],bbox[1] - 20),cv.FONT_HERSHEY_PLAIN,2,(255,0,255),2)
                
                my_path = 'Breach'
                if os.path.exists(my_path):
                    os.chdir(my_path)
                    cv.imwrite(filename="breach.jpg", img=frame)
                
                    
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            localtime = time.ctime()
            # lt = localtime.replace(" ", "")

            cv.putText(frame,f'FPS: {int(fps)}',(10,50),cv.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
            cv.putText(frame,f'{localtime}',(300,470),cv.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),1)
            
            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
           
            # camera.release()            //use if you pass second parameter in cv.videocapture
            # cv.destroyAllWindows()      //use if you pass second parameter in cv.videocapture
            
    
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



# for image
upload_folder = "Images/"
if not os.path.exists(upload_folder):
    os.mkdir(upload_folder)
            
app.config['UPLOAD_FOLDER'] = upload_folder
allowed_extensions = ['jpg','png','jpeg']

def check_extension(filename):
    return filename.split('.')[-1] in allowed_extensions

@app.route('/imagedir',methods=['GET','POST'])
def imagedir():
    if not session.get('username'):
        return redirect(url_for('login'))
    form = AddPersonForm()
    if form.validate_on_submit():
        name = form.name.data
        files = form.image.data
        # if not os.path.exists('Images'):
        #     os.mkdir('Images')
        #     os.chdir('Images')
        #     os.mkdir(name)
        for file in files:
            file_filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],file_filename))
        # if not os.path.exists('Images'):
        #     os.mkdir('Images')
        #     os.chdir('Images')
        #     os.mkdir(name)
                #cv.imwrite(filename=f'{count}.jpg', img=file)
                
        
    return render_template('imageform.html',form=form,title="Add Person")


@app.route("/",methods=['GET','POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.user.data
        password = form.password.data
        
        if  username == 'Badri' and password == 'Badri123':
            flash("You are successfully logged in!!","success")
            session['username'] = username
            return redirect("/index")
        else:
            flash("Sorry, Something went wrong!!","danger")
    return render_template("login.html",form=form,title="Login")

@app.route("/logout")
def logout():
    session['user_id'] = False
    session.pop('username',None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)