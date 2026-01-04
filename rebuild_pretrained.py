"""
Alternative approach: Load EfficientNet with pretrained weights first,
then load the h5 weights on top
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import keras
from keras import layers
from keras.applications import EfficientNetB0
import zipfile

MODEL_PATH = "best_model_ultrafast.keras"

# Model specs
SEQUENCE_LENGTH = 10
IMG_SIZE = 112
NUM_CLASSES = 50

def build_model_with_pretrained():
    """Build model with ImageNet pretrained EfficientNet"""
    inputs = layers.Input(shape=(SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3), name="input_layer_9")
    
    # Use pretrained weights as starting point
    base_model = EfficientNetB0(
        include_top=False,
        weights='imagenet',  # Start with pretrained
        pooling='avg',
        input_shape=(IMG_SIZE, IMG_SIZE, 3)
    )
    base_model.trainable = False
    
    x = layers.TimeDistributed(base_model, name="time_distributed_4")(inputs)
    x = layers.BatchNormalization(name="batch_normalization_4")(x)
    x = layers.LSTM(64, return_sequences=False, name="lstm_5")(x)
    x = layers.Dropout(0.4, name="dropout_9")(x)
    x = layers.Dense(128, activation='relu', name="dense_8")(x)
    x = layers.Dropout(0.4, name="dropout_10")(x)
    outputs = layers.Dense(NUM_CLASSES, activation='softmax', name="dense_9")(x)
    
    return keras.Model(inputs=inputs, outputs=outputs, name="functional_4")

print("Building model with ImageNet pretrained weights...")
model = build_model_with_pretrained()
print(f"Model built. Input: {model.input_shape}, Output: {model.output_shape}")

# Now load just the trainable layer weights (BatchNorm, LSTM, Dense)
print("\n=== Loading trainable weights from original model ===")

with zipfile.ZipFile(MODEL_PATH, 'r') as z:
    z.extract('model.weights.h5', '.')

# Load entire weights file and let keras match what it can
try:
    print("Loading weights with skip_mismatch=True...")
    model.load_weights('model.weights.h5', skip_mismatch=True)
    print("Weights loaded!")
except Exception as e:
    print(f"Load error: {e}")

# Test prediction 
print("\n=== Testing prediction ===")
# Create different test images to see if predictions vary
for i in range(3):
    # Create distinctly different test inputs
    if i == 0:
        test_input = np.zeros((1, SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3), dtype=np.float32)
    elif i == 1:
        test_input = np.ones((1, SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3), dtype=np.float32)
    else:
        test_input = np.random.rand(1, SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3).astype(np.float32)
    
    pred = model.predict(test_input, verbose=0)
    top_idx = np.argmax(pred)
    print(f"Test {i+1}: Top prediction index={top_idx}, confidence={pred[0][top_idx]*100:.2f}%")

# Save model
print("\nSaving model with pretrained backbone...")
model.save('rebuilt_model_pretrained.keras')
print("Saved to rebuilt_model_pretrained.keras")

os.remove('model.weights.h5')
