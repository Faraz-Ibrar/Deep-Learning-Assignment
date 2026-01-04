"""
Inspect weights file to understand exact architecture
"""
import zipfile
import h5py
import numpy as np

MODEL_PATH = "best_model_ultrafast.keras"

# Extract weights
with zipfile.ZipFile(MODEL_PATH, 'r') as z:
    z.extract('model.weights.h5', '.')

# Inspect weights
with h5py.File('model.weights.h5', 'r') as f:
    def print_structure(name, obj):
        if isinstance(obj, h5py.Dataset):
            print(f"  {name}: shape={obj.shape}, dtype={obj.dtype}")
    
    print("=== WEIGHTS FILE STRUCTURE ===\n")
    
    # Print all groups and their contents
    def explore(group, prefix=""):
        for key in group.keys():
            item = group[key]
            if isinstance(item, h5py.Group):
                print(f"{prefix}{key}/")
                explore(item, prefix + "  ")
            elif isinstance(item, h5py.Dataset):
                print(f"{prefix}{key}: shape={item.shape}")
    
    explore(f)
    
    # Focus on LSTM and Dense layers
    print("\n\n=== KEY LAYER SHAPES ===")
    
    # Look for specific layers
    for layer_name in ['lstm_5', 'lstm_6', 'dense_8', 'dense_9', 'batch_normalization_4']:
        if layer_name in f:
            print(f"\n{layer_name}:")
            layer = f[layer_name]
            explore(layer, "  ")

import os
os.remove('model.weights.h5')
