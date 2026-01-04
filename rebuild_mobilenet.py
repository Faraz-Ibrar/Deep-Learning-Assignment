"""
Rebuild MobileNetV2 model and load weights manually to bypass Keras 3.x loading errors
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import keras
from keras import layers
from keras.applications import MobileNetV2
import zipfile
import h5py

WEIGHTS_PATH = "final_model_fast_50_classes.keras"
TARGET_PATH = "rebuilt_mobilenet.keras"

SEQUENCE_LENGTH = 12
IMG_SIZE = 128
NUM_CLASSES = 50

def build_model():
    print("Building model architecture...")
    inputs = layers.Input(shape=(SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3), name="input_layer")
    
    # Base MobileNetV2
    # Note: alphas=1.0 is standard. input_shape must match.
    base_model = MobileNetV2(
        include_top=False,
        weights='imagenet',
        pooling='avg',
        input_shape=(IMG_SIZE, IMG_SIZE, 3)
    )
    base_model.trainable = False
    
    x = layers.TimeDistributed(base_model, name="time_distributed")(inputs)
    x = layers.BatchNormalization(name="batch_normalization")(x)
    
    # LSTM 1 - 128 units, return sequences
    x = layers.LSTM(128, return_sequences=True, name="lstm")(x)
    x = layers.Dropout(0.4, name="dropout")(x)
    
    # LSTM 2 - 64 units, no return sequences
    x = layers.LSTM(64, return_sequences=False, name="lstm_1")(x)
    x = layers.Dropout(0.4, name="dropout_1")(x)
    
    # Dense 1 - 256 units
    x = layers.Dense(256, activation='relu', name="dense")(x)
    x = layers.Dropout(0.4, name="dropout_2")(x)
    
    # Output - 50 units
    outputs = layers.Dense(NUM_CLASSES, activation='softmax', name="dense_1")(x)
    
    model = keras.Model(inputs=inputs, outputs=outputs, name="rebuilt_mobilenet")
    return model

print("Initializing model...")
model = build_model()
print("Model built initialized with ImageNet weights")

# Extract weights from source file
print(f"Extracting weights from {WEIGHTS_PATH}...")
with zipfile.ZipFile(WEIGHTS_PATH, 'r') as z:
    z.extract('model.weights.h5', '.')

print("Mapping and loading weights...")
with h5py.File('model.weights.h5', 'r') as f:
    h5_weights = {}
    
    # Index all weights in the file
    def visit_item(name, obj):
        if isinstance(obj, h5py.Dataset):
            h5_weights[name] = (obj.shape, obj[()])
            # Also index by suffix for fuzzy matching
            parts = name.split('/')
            if 'vars' in parts:
                idx = parts.index('vars')
                if idx > 0:
                    layer_name = parts[idx-1] # e.g. stem_conv
                    var_idx = parts[-1]
                    
                    # Heuristic for variable types based on index
                    # This works for most Keras layers but strict checking is better
                    suffix = "unknown"
                    if var_idx == '0': suffix = "kernel" # or gamma
                    elif var_idx == '1': suffix = "bias" # or beta
                    elif var_idx == '2': suffix = "moving_mean"
                    elif var_idx == '3': suffix = "moving_variance"
                    
                    # Refined mapping
                    if 'batch_normaliz' in layer_name:
                         if var_idx=='0': suffix='gamma'
                         elif var_idx=='1': suffix='beta'
                         elif var_idx=='2': suffix='moving_mean'
                         elif var_idx=='3': suffix='moving_variance'
                    
                    key = f"{layer_name}/{suffix}"
                    h5_weights[key] = (obj.shape, obj[()])
    
    f.visititems(visit_item)
    print(f"Found {len(h5_weights)} weight entries in H5")

    # Load into model
    stats = {'loaded': 0, 'total': 0}
    
    def process_layer(l):
        if hasattr(l, 'layers'):
            for sub in l.layers:
                process_layer(sub)
            return

        weights = l.weights
        if not weights: return
        
        new_weights = []
        layer_loaded = False
        
        for w in weights:
            stats['total'] += 1
            w_shape = w.shape
            w_name = w.name.split(':')[0]
            parts = w_name.split('/')
            
            target_layer = parts[-2] if len(parts) > 1 else parts[0]
            target_type = parts[-1]
            
            match = None
            
            # 1. Exact Name Match in Index
            key = f"{target_layer}/{target_type}"
            if key in h5_weights:
                shape, val = h5_weights[key]
                if shape == w_shape:
                    match = val
            
            # 2. Fuzzy Match
            if match is None:
                for k, (shape, val) in h5_weights.items():
                    if target_layer in k and shape == w_shape:
                        if target_type in k or \
                           (target_type=='kernel' and '0' in k) or \
                           (target_type=='bias' and '1' in k):
                            match = val
                            break
            
            if match is not None:
                new_weights.append(match)
                layer_loaded = True
            else:
                new_weights.append(w.numpy())
        
        if layer_loaded and len(new_weights) == len(weights):
            l.set_weights(new_weights)
            stats['loaded'] += len(weights)

    for layer in model.layers:
        process_layer(layer)
        
    print(f"\nMatched and loaded {stats['loaded']}/{stats['total']} weight tensors")

# Save rebuilt model
model.save(TARGET_PATH)
print(f"Saved rebuilt model to {TARGET_PATH}")

if os.path.exists('model.weights.h5'):
    os.remove('model.weights.h5')
