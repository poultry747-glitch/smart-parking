from flask import Flask, render_template, Response, jsonify
import cv2
import pickle
import numpy as np
from keras.models import load_model
import atexit
import signal
import sys
import os

# Set TensorFlow to use single-threaded execution to avoid multiprocessing issues
os.environ['TF_NUM_INTEROP_THREADS'] = '1'
os.environ['TF_NUM_INTRAOP_THREADS'] = '1'

app = Flask(__name__)

# Production configuration
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

model = load_model('model_final.h5')

class_dictionary = {0: 'no_car', 1: 'car'}

cap = cv2.VideoCapture('car_test.mp4')

with open('carposition.pkl', 'rb') as f:
    posList = pickle.load(f)

width, height = 130, 65

def cleanup_resources():
    """Clean up resources when the application shuts down"""
    try:
        if cap is not None and cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
        print("Resources cleaned up successfully")
    except Exception as e:
        print(f"Error during cleanup: {e}")

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print(f"Received signal {signum}, cleaning up...")
    cleanup_resources()
    sys.exit(0)

# Register cleanup handlers
atexit.register(cleanup_resources)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def checkParkingSpace(img):
    spaceCounter = 0
    imgCrops = []

    for pos in posList:
        x, y = pos
        imgCrop = img[y:y + height, x:x + width]
        imgResize = cv2.resize(imgCrop, (48, 48))
        imgNormalized = imgResize / 255.0
        imgCrops.append(imgNormalized)

    imgCrops = np.array(imgCrops)
    
    # Use predict with verbose=0 to reduce output and potential multiprocessing issues
    predictions = model.predict(imgCrops, verbose=0)

    for i, pos in enumerate(posList):
        x, y = pos
        inID = np.argmax(predictions[i])
        label = class_dictionary[inID]

        if label == 'no_car':
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
            textColor = (0,0,0)
        else:
            color = (0, 0, 255)
            thickness = 2
            textColor = (255,255,255)

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        font_scale = 0.5
        text_thickness = 1
        
        textSize = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_thickness)[0]
        textX = x
        textY = y + height - 5
        cv2.rectangle(img, (textX, textY - textSize[1] - 5), (textX + textSize[0] + 6, textY + 2), color, -1)
        cv2.putText(img, label, (textX + 3, textY - 3), cv2.FONT_HERSHEY_SIMPLEX, font_scale, textColor, text_thickness)

    totalSpaces = len(posList)


    return img, spaceCounter, totalSpaces - spaceCounter

def generate_frames():
    while True:
        if not cap.isOpened():
            break
            
        success, img = cap.read()
        if not success:
            # Reset video to beginning for continuous loop
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        img = cv2.resize(img, (1280, 720))
        img, free_spaces, occupied_spaces = checkParkingSpace(img)
        ret, buffer = cv2.imencode('.jpg', img)
        if not ret:
            continue
            
        img = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/space_count')
def space_count():
    if not cap.isOpened():
        return jsonify(free=0, occupied=0, error="Video capture not available")
        
    success, img = cap.read()
    if success:
        img = cv2.resize(img, (1280, 720))
        _, free_spaces, occupied_spaces = checkParkingSpace(img)
        return jsonify(free=free_spaces, occupied=occupied_spaces)
    return jsonify(free=0, occupied=0, error="Failed to read frame")

if __name__ == "__main__":
    try:
        print("Starting Smart Parking application...")
        # Get port from environment variable (Railway provides this)
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False, threaded=True)
    except KeyboardInterrupt:
        print("Application interrupted by user")
    finally:
        cleanup_resources()
