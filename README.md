---
title: Smart Parking Space Detection
emoji: 🚗
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# 🚗 Smart Parking Space Detection System

An AI-powered computer vision application that analyzes parking lot images and videos to detect available and occupied parking spaces in real-time.

## 🎯 Features

- **Real-time Detection**: Instant analysis of parking space availability
- **High Accuracy**: 95%+ accuracy using CNN with VGG16 transfer learning
- **Visual Feedback**: Color-coded bounding boxes (Green = Free, Red = Occupied)
- **Confidence Scores**: Each prediction includes confidence percentage
- **Multiple Input Types**: Support for both images and videos
- **Statistics Dashboard**: Occupancy rate and space count analytics

## 🔧 How to Use

1. **Upload an Image**: Select a parking lot image in the "Image Analysis" tab
2. **Upload a Video**: Select a parking lot video in the "Video Analysis" tab
3. **Click Analyze**: The system will automatically process and highlight parking spaces
4. **View Results**: See free (green) and occupied (red) spaces with statistics

## 🛠️ Technical Details

### Model Architecture
- **Base Model**: VGG16 with transfer learning
- **Input Size**: 48x48 pixels per parking space
- **Output**: Binary classification (occupied/free)
- **Framework**: TensorFlow/Keras

### Computer Vision Pipeline
1. **Image Preprocessing**: Resize and normalize input images
2. **ROI Extraction**: Extract individual parking space regions
3. **Model Inference**: CNN prediction for each space
4. **Post-processing**: Apply confidence thresholds and generate visualizations

### Performance
- **Accuracy**: 95%+ on test dataset
- **Processing Speed**: Real-time inference
- **Model Size**: ~105MB (optimized for deployment)

## 📊 Use Cases

- **Smart Cities**: Automated parking management systems
- **Shopping Malls**: Real-time parking availability for customers
- **Airports**: Efficient parking space utilization
- **Office Buildings**: Employee parking optimization
- **Event Management**: Large-scale parking coordination

## 🔬 Model Training Details

The model was trained on a comprehensive dataset of parking lot images with the following specifications:

- **Training Data**: 1000+ labeled parking space images
- **Validation Split**: 80/20 train-validation split
- **Data Augmentation**: Rotation, zoom, horizontal flip, brightness adjustment
- **Optimizer**: SGD with momentum (0.9)
- **Learning Rate**: 0.0001
- **Epochs**: 15 with early stopping

## 🚀 Deployment

This application is deployed on Hugging Face Spaces using:
- **Runtime**: Python 3.8+
- **Interface**: Gradio for interactive web UI
- **Dependencies**: TensorFlow, OpenCV, NumPy, Pillow

## 🎨 Interface Features

### Image Analysis Tab
- Upload parking lot images (JPG, PNG)
- Real-time processing and visualization
- Detailed statistics and occupancy rates

### Video Analysis Tab
- Upload parking lot videos (MP4, AVI)
- First-frame analysis with full statistics
- Future: Frame-by-frame processing capabilities

## 🔍 Example Results

The system provides:
- **Visual Output**: Annotated image with colored bounding boxes
- **Free Spaces**: Count of available parking spots
- **Occupied Spaces**: Count of taken parking spots
- **Occupancy Rate**: Percentage calculation
- **Confidence Scores**: Model prediction confidence for each space

## 🤝 Contributing

This project demonstrates the application of computer vision and deep learning for smart city solutions. Feel free to:

- Report issues or suggest improvements
- Contribute to model optimization
- Extend functionality for different parking lot layouts
- Add support for real-time video streaming

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- VGG16 architecture by Visual Geometry Group, Oxford
- TensorFlow and Keras for deep learning framework
- OpenCV for computer vision operations
- Hugging Face for deployment platform

---

*Developed with ❤️ for smart city solutions and intelligent transportation systems.*