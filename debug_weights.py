"""
Debug weight loading - check which layers loaded correctly
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import keras
from keras import layers
from keras.applications import EfficientNetB0
import zipfile
import h5py

MODEL_PATH = "best_model_ultrafast.keras"

# Model specs
SEQUENCE_LENGTH = 10
IMG_SIZE = 112
NUM_CLASSES = 50

def build_model():
    inputs = layers.Input(shape=(SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3), name="input_layer_9")
    
    base_model = EfficientNetB0(
        include_top=False,
        weights=None,
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

print("Building model...")
model = build_model()

# Extract weights and check structure
print("\n=== CHECKING WEIGHTS FILE STRUCTURE ===")
with zipfile.ZipFile(MODEL_PATH, 'r') as z:
    z.extract('model.weights.h5', '.')

with h5py.File('model.weights.h5', 'r') as f:
    print("Top level keys:", list(f.keys()))
    
    # Check TimeDistributed layer structure
    if 'time_distributed_4' in f:
        td = f['time_distributed_4']
        print("\nTimeDistributed layer keys:", list(td.keys()))
        if 'efficientnetb0' in td:
            eff = td['efficientnetb0']
            print("EfficientNet keys (first 10):", list(eff.keys())[:10])

# Check model layer names
print("\n=== MODEL LAYER NAMES (TimeDistributed inner) ===")
td_layer = model.get_layer('time_distributed_4')
inner_model = td_layer.layer
print(f"Inner model name: {inner_model.name}")
print(f"Inner model layer names (first 10): {[l.name for l in inner_model.layers[:10]]}")

# Try loading with by_name
print("\n\n=== TRYING WEIGHT LOADING ===")
try:
    model.load_weights('model.weights.h5', by_name=True, skip_mismatch=True)
    print("Loaded with by_name=True, skip_mismatch=True")
except Exception as e:
    print(f"Error: {e}")

# Check if EfficientNet weights are non-zero
print("\n=== CHECKING IF EFFICIENTNET WEIGHTS LOADED ===")
stem_conv = None
for layer in inner_model.layers:
    if 'stem_conv' in layer.name.lower() or 'conv2d' in layer.name.lower():
        if hasattr(layer, 'kernel'):
            weights = layer.kernel.numpy()
            print(f"{layer.name}: mean={weights.mean():.6f}, std={weights.std():.6f}")
            if abs(weights.mean()) < 0.0001 and weights.std() < 0.1:
                print("  ^ WARNING: Weights may be uninitialized!")
            break

# Check LSTM weights
print("\n=== CHECKING LSTM WEIGHTS ===")
lstm = model.get_layer('lstm_5')
kernel = lstm.kernel.numpy()
print(f"LSTM kernel: mean={kernel.mean():.6f}, std={kernel.std():.6f}")

# Check Dense weights  
print("\n=== CHECKING DENSE WEIGHTS ===")
dense8 = model.get_layer('dense_8')
dense9 = model.get_layer('dense_9')
print(f"Dense8 kernel: mean={dense8.kernel.numpy().mean():.6f}, std={dense8.kernel.numpy().std():.6f}")
print(f"Dense9 kernel: mean={dense9.kernel.numpy().mean():.6f}, std={dense9.kernel.numpy().std():.6f}")

os.remove('model.weights.h5')
