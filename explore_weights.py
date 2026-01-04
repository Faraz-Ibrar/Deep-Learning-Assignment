"""
Explore the exact structure of the weights file
"""
import zipfile
import h5py

MODEL_PATH = "best_model_ultrafast.keras"

with zipfile.ZipFile(MODEL_PATH, 'r') as z:
    z.extract('model.weights.h5', '.')

with h5py.File('model.weights.h5', 'r') as f:
    print("=== FULL STRUCTURE ===\n")
    
    def print_structure(name, obj):
        indent = "  " * name.count('/')
        if isinstance(obj, h5py.Dataset):
            print(f"{indent}{name}: shape={obj.shape}")
        else:
            print(f"{indent}{name}/")
    
    f.visititems(print_structure)

import os
os.remove('model.weights.h5')
