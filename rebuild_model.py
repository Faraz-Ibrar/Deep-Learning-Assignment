"""
Rebuild model with EXACT architecture from config.json
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import tensorflow as tf
import keras
from keras import layers
from keras.applications import EfficientNetB0
import zipfile

MODEL_PATH = "best_model_ultrafast.keras"

# Model specs from config.json
SEQUENCE_LENGTH = 10
IMG_SIZE = 112
NUM_CLASSES = 50

def build_model():
    """Rebuild the model architecture EXACTLY as in config.json"""
    
    # Input layer: (batch, 10, 112, 112, 3)
    inputs = layers.Input(shape=(SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3), name="input_layer_9")
    
    # TimeDistributed EfficientNetB0
    base_model = EfficientNetB0(
        include_top=False,
        weights=None,
        pooling='avg',
        input_shape=(IMG_SIZE, IMG_SIZE, 3)
    )
    base_model.trainable = False
    
    # Wrap in TimeDistributed - output shape: (batch, 10, 1280)
    x = layers.TimeDistributed(base_model, name="time_distributed_4")(inputs)
    
    # BatchNormalization - output shape: (batch, 10, 1280)
    x = layers.BatchNormalization(name="batch_normalization_4")(x)
    
    # LSTM: 64 units, return_sequences=False - output shape: (batch, 64)
    x = layers.LSTM(64, return_sequences=False, name="lstm_5")(x)
    
    # Dropout 0.4
    x = layers.Dropout(0.4, name="dropout_9")(x)
    
    # Dense: 128 units, relu - output shape: (batch, 128)
    x = layers.Dense(128, activation='relu', name="dense_8")(x)
    
    # Dropout 0.4
    x = layers.Dropout(0.4, name="dropout_10")(x)
    
    # Dense: 50 units, softmax - output shape: (batch, 50)
    outputs = layers.Dense(NUM_CLASSES, activation='softmax', name="dense_9")(x)
    
    model = keras.Model(inputs=inputs, outputs=outputs, name="functional_4")
    
    return model

print("Building model with EXACT architecture...")
model = build_model()
model.summary()

print(f"\nModel input shape: {model.input_shape}")
print(f"Model output shape: {model.output_shape}")

# Extract weights from .keras file and load
print("\n\nExtracting weights from .keras file...")
try:
    with zipfile.ZipFile(MODEL_PATH, 'r') as z:
        z.extract('model.weights.h5', '.')
    
    # Try loading weights
    print("Loading weights...")
    model.load_weights('model.weights.h5')
    print("\n✅ Weights loaded successfully!")
    
    # Test prediction
    print("\nTesting prediction with random input...")
    test_input = np.random.rand(1, SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3).astype(np.float32)
    pred = model.predict(test_input, verbose=0)
    print(f"Prediction shape: {pred.shape}")
    print(f"Sum of predictions: {pred.sum():.4f}")
    print(f"Max confidence: {pred.max()*100:.2f}%")
    print(f"Top prediction index: {np.argmax(pred)}")
    print(f"Top 5 class indices: {np.argsort(pred[0])[-5:][::-1]}")
    print(f"Top 5 confidences: {[f'{c*100:.2f}%' for c in np.sort(pred[0])[-5:][::-1]]}")
    
    # Save the rebuilt model
    print("\nSaving correctly rebuilt model...")
    model.save('rebuilt_model_correct.keras')
    print("✅ Model saved to rebuilt_model_correct.keras")
    
    # Cleanup
    os.remove('model.weights.h5')
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    
    if os.path.exists('model.weights.h5'):
        os.remove('model.weights.h5')
