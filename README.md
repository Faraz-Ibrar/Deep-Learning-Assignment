# Deep Learning Assignment: Action Recognition System

## Team Members
* **Faraz Ibrar** (221327)
* **Amir Hamza** (221318)

## Project Overview
This project is an advanced Action Recognition System capable of identifying 50 different human activities from video sequences or images. It uses a deep learning model integrated into a modern web application to provide real-time predictions.

## How It Works

### Model Architecture
The core of the system is a **LRCN (Long-term Recurrent Convolutional Network)** which combines:
1. **CNN (MobileNetV2)**: Acts as a feature extractor. It processes each frame of the input video independently to extract high-level visual features. It is wrapped in a `TimeDistributed` layer to handle video sequences.
2. **RNN (LSTM)**: Two layers of Long Short-Term Memory (LSTM) networks process the sequence of features extracted by the CNN. This allows the model to understand temporal dynamics and motion patterns over time.
3. **Classification Head**: Dense layers that output the probability for each of the 50 action classes.

**Input Specification:**
* Sequence Length: 12 frames
* Image Resolution: 128x128 pixels
* Channels: 3 (RGB)

### Technical Stack
* **frontend**: Built with React.js, Tailwind CSS, and Framer Motion for a responsive and animated user interface.
* **backend**: Built with FastAPI (Python) to serve the Keras model and handle image preprocessing.

## Installation & Running

### Prerequisites
* Python 3.9+
* Node.js & npm

### 1. Setup Backend
```bash
cd backend
# Install dependencies
pip install tensorflow fastapi uvicorn python-multipart pillow opencv-python tf-keras

# Run the server
uvicorn main:app --reload
```
The backend will run on `http://localhost:8000`.

### 2. Setup Frontend
```bash
cd action-recognition-app
# Install dependencies
npm install

# Run the development server
npm run dev
```
The frontend will run on `http://localhost:5173`.

## Usage
1. Open the web application.
2. Upload an image or select a sample.
3. The system creates a temporal sequence from the image and feeds it to the model.
4. View the top predictions with confidence scores.
