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
*  
 
 
 
 
 
 
 
 
   
 

 


### Technical Stack
* **frontend**: Built with React.js, Tailwind CSS, and Framer Motion for a responsive and animated user interface.
* **backend**: Built with FastAPI (Python) to serve the Keras model and handle image preprocessing.

## Installation & Running

### Prerequisites
* Python 3.9+
* Node.js & npm

<img width="940" height="312" alt="image" src="https://github.com/user-attachments/assets/50f15e37-4051-4678-bdd8-45613dacc4ea" />
<img width="940" height="523" alt="image" src="https://github.com/user-attachments/assets/90f39012-d680-44bb-ba58-cc33d00474a6" />
<img width="940" height="353" alt="image" src="https://github.com/user-attachments/assets/d893e69e-2ebf-4b9e-842f-e02f66e259b6" />
<img width="940" height="383" alt="image" src="https://github.com/user-attachments/assets/fd066f00-e18d-4c2e-94e5-c45f9bf9414b" />
<img width="940" height="374" alt="image" src="https://github.com/user-attachments/assets/50d2dafe-223d-40ee-998d-d0b5af8837fc" />
<img width="940" height="364" alt="image" src="https://github.com/user-attachments/assets/a9fc14a4-6cbb-4979-9c35-8419c508f4b6" />
<img width="940" height="384" alt="image" src="https://github.com/user-attachments/assets/e9cafcd3-3106-4e6a-875c-266c7bf07dd0" />
<img width="940" height="367" alt="image" src="https://github.com/user-attachments/assets/86292cf0-1a70-4d40-b656-bd7300a6e11a" />
<img width="940" height="464" alt="image" src="https://github.com/user-attachments/assets/f103b2f0-2eaf-4ef6-95e2-f5cd494b0b5b" />
<img width="940" height="420" alt="image" src="https://github.com/user-attachments/assets/ec617b0e-937e-488c-b4cb-1f5ec19105b6" />
<img width="940" height="484" alt="image" src="https://github.com/user-attachments/assets/6d97e37a-69ee-4a91-8e1f-8af394ba3b2b" />
<img width="940" height="444" alt="image" src="https://github.com/user-attachments/assets/1750f678-3a01-4265-8a5c-ea3f60f81de9" />
<img width="940" height="247" alt="image" src="https://github.com/user-attachments/assets/114ac1ad-2d0a-4c76-91d5-67459e335aef" />

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
