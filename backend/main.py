"""
Action Recognition API
FastAPI backend for the UCF101 action recognition model
"""

import os
import io
import numpy as np
import cv2
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tensorflow as tf

# Initialize FastAPI app
app = FastAPI(
    title="Action Recognition API",
    description="API for predicting human actions from images using a trained UCF101 model",
    version="1.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Action class names (must match training order - 50 classes)
ACTION_NAMES = [
    'ApplyEyeMakeup',
    'ApplyLipstick',
    'Archery',
    'BabyCrawling',
    'BalanceBeam',
    'BandMarching',
    'BaseballPitch',
    'Basketball',
    'BasketballDunk',
    'BenchPress',
    'Biking',
    'Billiards',
    'BlowDryHair',
    'BlowingCandles',
    'Bowling',
    'BoxingPunchingBag',
    'BoxingSpeedBag',
    'BreastStroke',
    'BrushingTeeth',
    'CleanAndJerk',
    'CliffDiving',
    'CricketBowling',
    'CricketShot',
    'Diving',
    'Drumming',
    'Fencing',
    'FloorGymnastics',
    'FrisbeeCatch',
    'GolfSwing',
    'Haircut',
    'Hammering',
    'HandstandPushups',
    'HighJump',
    'HorseRiding',
    'HulaHoop',
    'IceDancing',
    'JavelinThrow',
    'JugglingBalls',
    'JumpingJack',
    'Kayaking',
    'Knitting',
    'LongJump',
    'Lunges',
    'MoppingFloor',
    'ParallelBars',
    'PlayingGuitar',
    'PlayingPiano',
    'PlayingViolin',
    'PushUps',
    'Skiing'
]

# Model path - using the manually rebuilt MobileNetV2 model (safest option)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "rebuilt_mobilenet.keras")

# Global model variable
model = None


def load_model():
    """Load the Keras model on startup"""
    global model
    if model is None:
        print(f"Loading model from: {MODEL_PATH}")
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        
        # Load the rebuilt model directly with keras
        import keras
        model = keras.models.load_model(MODEL_PATH, compile=False)
        print("Model loaded successfully!")
        print(f"Model input shape: {model.input_shape}")
        print(f"Model output shape: {model.output_shape}")
    
    return model


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Preprocess an uploaded image for model prediction.
    
    Model specs (MobileNetV2 + LSTM):
    - Input Shape: (batch_size, 12, 128, 128, 3)
    - Sequence Length: 12 frames
    - Image Size: 128 × 128 pixels
    - Channels: 3 (RGB)
    
    Args:
        image_bytes: Raw bytes of the uploaded image
        
    Returns:
        Preprocessed numpy array with shape (1, 12, 128, 128, 3)
    """
    # Step 1: Load image from bytes
    image = Image.open(io.BytesIO(image_bytes))
    
    # Convert to RGB if necessary (handles PNG with alpha, grayscale, etc.)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Step 2: Resize to 128x128 (matching model input spec)
    image = image.resize((128, 128))
    
    # Step 3: Convert to array
    img_array = np.array(image)
    
    # Step 4: Use MobileNetV2 preprocessing (scales to -1 to 1 range)
    from keras.applications.mobilenet_v2 import preprocess_input
    img_array = img_array.astype(np.float32)
    img_array = preprocess_input(img_array)
    
    # Step 5: Create sequence (repeat the image 12 times)
    sequence = np.array([img_array] * 12)
    
    # Step 6: Add batch dimension
    input_data = np.expand_dims(sequence, axis=0)  # Shape: (1, 12, 128, 128, 3)
    
    return input_data


@app.on_event("startup")
async def startup_event():
    """Load model when the server starts"""
    try:
        load_model()
    except Exception as e:
        print(f"Warning: Could not load model on startup: {e}")
        print("Model will be loaded on first prediction request.")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Action Recognition API is running",
        "endpoints": {
            "predict": "/predict",
            "health": "/health",
            "actions": "/actions"
        }
    }


@app.get("/health")
async def health_check():
    """Check if the model is loaded and ready"""
    global model
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_path": MODEL_PATH,
        "num_classes": len(ACTION_NAMES)
    }


@app.get("/actions")
async def get_actions():
    """Get list of supported action classes"""
    return {
        "actions": ACTION_NAMES,
        "count": len(ACTION_NAMES)
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict the action in an uploaded image.
    
    Args:
        file: Uploaded image file (JPEG, PNG, etc.)
        
    Returns:
        JSON with predictions sorted by confidence
    """
    global model
    
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Allowed: {allowed_types}"
        )
    
    try:
        # Load model if not already loaded
        if model is None:
            load_model()
        
        # Read image bytes
        image_bytes = await file.read()
        
        # Preprocess image
        input_data = preprocess_image(image_bytes)
        
        # Make prediction
        predictions = model.predict(input_data, verbose=0)
        
        # Get probabilities (assuming softmax output)
        probabilities = predictions[0]
        
        # Create results with action names and confidences
        results = []
        for idx, prob in enumerate(probabilities):
            results.append({
                "rank": 0,  # Will be set after sorting
                "action": ACTION_NAMES[idx],
                "confidence": round(float(prob) * 100, 2)  # Convert to percentage
            })
        
        # Sort by confidence (descending)
        results.sort(key=lambda x: x["confidence"], reverse=True)
        
        # Add ranks after sorting
        for i, result in enumerate(results):
            result["rank"] = i + 1
        
        return JSONResponse(content={
            "success": True,
            "filename": file.filename,
            "predictions": results,
            "top_prediction": {
                "action": results[0]["action"],
                "confidence": results[0]["confidence"]
            }
        })
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
