"""
UNIVERSAL WEIGHT LOADER: Robust Version
Matches weights by name similarity + shape to recover weights from broken H5
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import keras
import zipfile
import h5py

MODEL_PATH = "rebuilt_model_correct.keras"
WEIGHTS_PATH = "best_model_ultrafast.keras"

print("Loading target model...")
model = keras.models.load_model(MODEL_PATH)

print("Extracting weights...")
with zipfile.ZipFile(WEIGHTS_PATH, 'r') as z:
    z.extract('model.weights.h5', '.')

print("Mapping weights...")
with h5py.File('model.weights.h5', 'r') as f:
    h5_weights = {}
    
    def visit_item(name, obj):
        if isinstance(obj, h5py.Dataset):
            parts = name.split('/')
            h5_weights[name] = (obj.shape, obj[()])
            
            # Index by various suffixes for matching
            # e.g. "stem_conv/kernel"
            if 'vars' in parts:
                idx = parts.index('vars')
                if idx > 0:
                    layer_name = parts[idx-1]
                    var_idx = parts[-1]
                    suffix = "kernel" if var_idx == '0' else "bias"
                    # Handle special batchnorm indices
                    if 'batch_normaliz' in layer_name:
                         if var_idx=='0': suffix='gamma'
                         elif var_idx=='1': suffix='beta'
                         elif var_idx=='2': suffix='moving_mean'
                         elif var_idx=='3': suffix='moving_variance'
                    
                    key = f"{layer_name}/{suffix}"
                    h5_weights[key] = (obj.shape, obj[()])
    
    f.visititems(visit_item)
    print(f"Found {len(h5_weights)} weight entries in H5")
    
    # Iterate and Load
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
            
            # Determine target signature
            # e.g. stem_conv/kernel
            target_layer = parts[-2] if len(parts) > 1 else parts[0]
            target_type = parts[-1] # kernel, bias, etc
            
            match = None
            
            # 1. Exact Name/Suffix Match
            key = f"{target_layer}/{target_type}"
            if key in h5_weights:
                shape, val = h5_weights[key]
                if shape == w_shape:
                    match = val
            
            # 2. Fuzzy Match
            if match is None:
                for k, (shape, val) in h5_weights.items():
                    if target_layer in k and shape == w_shape:
                        # Check type
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

os.remove('model.weights.h5')

# Verify
print("\n=== VERIFICATION ===")
zeros = np.zeros((1, 10, 112, 112, 3), dtype=np.float32)
rand = np.random.rand(1, 10, 112, 112, 3).astype(np.float32)

p_zeros = model.predict(zeros, verbose=0)
p_rand = model.predict(rand, verbose=0)

idx_z = np.argmax(p_zeros)
idx_r = np.argmax(p_rand)

print(f"Zeros : Top={idx_z} ({p_zeros.max()*100:.1f}%)")
print(f"Random: Top={idx_r} ({p_rand.max()*100:.1f}%)")

if idx_z != idx_r:
    print("\n✅ SUCCESS: Predictions vary by input!")
else:
    print("\n⚠️ WARNING: Feature extractor might still be dead.")

model.save('rebuilt_model_universal.keras')
print("Saved to rebuilt_model_universal.keras")
