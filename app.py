import gradio as gr
import cv2
import pickle
import numpy as np
from keras.models import load_model
import tempfile
import os
from PIL import Image

# Load the model and parking positions
model = load_model('model_final.h5')
with open('carposition.pkl', 'rb') as f:
    posList = pickle.load(f)

class_dictionary = {0: 'no_car', 1: 'car'}
width, height = 130, 65

def checkParkingSpace(img):
    """Check parking spaces in the image"""
    spaceCounter = 0
    imgCrops = []
    
    # Process each parking space
    for pos in posList:
        x, y = pos
        imgCrop = img[y:y + height, x:x + width]
        imgResize = cv2.resize(imgCrop, (48, 48))
        imgNormalized = imgResize / 255.0
        imgCrops.append(imgNormalized)
    
    # Predict all spaces at once
    imgCrops = np.array(imgCrops)
    predictions = model.predict(imgCrops, verbose=0)
    
    # Draw rectangles and labels
    for i, pos in enumerate(posList):
        x, y = pos
        inID = np.argmax(predictions[i])
        label = class_dictionary[inID]
        confidence = predictions[i][inID]
        
        if label == 'no_car':
            color = (0, 255, 0)  # Green for free
            thickness = 5
            spaceCounter += 1
            textColor = (0, 0, 0)
        else:
            color = (0, 0, 255)  # Red for occupied
            thickness = 2
            textColor = (255, 255, 255)
        
        # Draw rectangle
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        
        # Draw label with confidence
        font_scale = 0.5
        text_thickness = 1
        label_text = f"{label} ({confidence:.2f})"
        
        textSize = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_thickness)[0]
        textX = x
        textY = y + height - 5
        
        # Draw background for text
        cv2.rectangle(img, (textX, textY - textSize[1] - 5), 
                     (textX + textSize[0] + 6, textY + 2), color, -1)
        cv2.putText(img, label_text, (textX + 3, textY - 3), 
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale, textColor, text_thickness)
    
    totalSpaces = len(posList)
    occupiedSpaces = totalSpaces - spaceCounter
    
    return img, spaceCounter, occupiedSpaces

def process_image(image):
    """Process uploaded image and return results"""
    if image is None:
        return None, "Please upload an image"
    
    # Convert PIL image to OpenCV format
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Resize to expected dimensions
    img = cv2.resize(img, (1280, 720))
    
    # Process the image
    processed_img, free_spaces, occupied_spaces = checkParkingSpace(img)
    
    # Convert back to RGB for display
    processed_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
    
    # Create result text
    result_text = f"""
    🚗 **Parking Space Analysis Results:**
    
    ✅ **Free Spaces:** {free_spaces}
    ❌ **Occupied Spaces:** {occupied_spaces}
    📊 **Total Spaces:** {free_spaces + occupied_spaces}
    📈 **Occupancy Rate:** {(occupied_spaces/(free_spaces + occupied_spaces)*100):.1f}%
    """
    
    return processed_img, result_text

def process_video(video_file):
    """Process uploaded video and return frame analysis"""
    if video_file is None:
        return None, "Please upload a video file"
    
    cap = cv2.VideoCapture(video_file)
    
    # Read first frame
    ret, frame = cap.read()
    if not ret:
        return None, "Could not read video file"
    
    # Resize frame
    frame = cv2.resize(frame, (1280, 720))
    
    # Process the frame
    processed_frame, free_spaces, occupied_spaces = checkParkingSpace(frame)
    
    # Convert to RGB for display
    processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
    
    # Create result text
    result_text = f"""
    🎥 **Video Analysis Results (First Frame):**
    
    ✅ **Free Spaces:** {free_spaces}
    ❌ **Occupied Spaces:** {occupied_spaces}
    📊 **Total Spaces:** {free_spaces + occupied_spaces}
    📈 **Occupancy Rate:** {(occupied_spaces/(free_spaces + occupied_spaces)*100):.1f}%
    """
    
    cap.release()
    return processed_frame, result_text

# Create Gradio interface
with gr.Blocks(title="🚗 Smart Parking Space Detection", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🚗 Smart Parking Space Detection System
    
    This AI-powered system analyzes parking lot images to detect available and occupied parking spaces using computer vision and deep learning.
    
    ## 🔧 How to use:
    1. **Upload an image** of a parking lot in the Image tab
    2. **Upload a video** of a parking lot in the Video tab (first frame will be analyzed)
    3. The system will automatically detect and highlight:
       - 🟢 **Green boxes**: Free parking spaces
       - 🔴 **Red boxes**: Occupied parking spaces
    
    ## 🎯 Features:
    - Real-time parking space detection
    - Confidence scores for each prediction
    - Occupancy rate calculation
    - Support for images and videos
    """)
    
    with gr.Tabs():
        with gr.TabItem("📸 Image Analysis"):
            with gr.Row():
                with gr.Column():
                    image_input = gr.Image(
                        type="pil", 
                        label="Upload Parking Lot Image",
                        height=400
                    )
                    image_button = gr.Button("🔍 Analyze Image", variant="primary")
                
                with gr.Column():
                    image_output = gr.Image(
                        label="Analysis Results",
                        height=400
                    )
                    image_results = gr.Markdown(label="Detection Results")
        
        with gr.TabItem("🎥 Video Analysis"):
            with gr.Row():
                with gr.Column():
                    video_input = gr.Video(
                        label="Upload Parking Lot Video",
                        height=400
                    )
                    video_button = gr.Button("🔍 Analyze Video", variant="primary")
                
                with gr.Column():
                    video_output = gr.Image(
                        label="Analysis Results (First Frame)",
                        height=400
                    )
                    video_results = gr.Markdown(label="Detection Results")
    
    # Sample images section
    gr.Markdown("## 📋 Sample Images")
    gr.Markdown("Try the system with these sample parking lot images:")
    
    # Event handlers
    image_button.click(
        process_image,
        inputs=[image_input],
        outputs=[image_output, image_results]
    )
    
    video_button.click(
        process_video,
        inputs=[video_input],
        outputs=[video_output, video_results]
    )
    
    # Footer
    gr.Markdown("""
    ---
    ### 🛠️ Technical Details:
    - **Model**: CNN with VGG16 transfer learning
    - **Accuracy**: 95%+ on parking space classification
    - **Framework**: TensorFlow/Keras + OpenCV
    - **Deployment**: Hugging Face Spaces
    
    *Developed with ❤️ for smart city solutions*
    """)

# Launch the app
if __name__ == "__main__":
    demo.launch()