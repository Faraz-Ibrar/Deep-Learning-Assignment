"""
ROBUST REBUILD:
1. Initialize with ImageNet weights (ensures feature extractor works)
2. Load user weights where possible (preserves training)
3. Keep ImageNet weights where user weights fail/mismatch
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
SEQUENCE_LENGTH = 10
IMG_SIZE = 112
NUM_CLASSES = 50

# 1. Build model with ImageNet weights
print("Building model with ImageNet initialization...")
inputs = layers.Input(shape=(SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3), name="input_layer")

# Start with ImageNet weights
base_model = EfficientNetB0(
    include_top=False,
    weights='imagenet', 
    pooling='avg',
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)
base_model.trainable = False

x = layers.TimeDistributed(base_model, name="time_distributed")(inputs)
x = layers.BatchNormalization(name="batch_normalization")(x)
x = layers.LSTM(64, return_sequences=False, name="lstm")(x)
x = layers.Dropout(0.4, name="dropout")(x)
x = layers.Dense(128, activation='relu', name="dense")(x)
x = layers.Dropout(0.4, name="dropout_1")(x)
outputs = layers.Dense(NUM_CLASSES, activation='softmax', name="dense_1")(x)

model = keras.Model(inputs=inputs, outputs=outputs)
print("Model built initialized with ImageNet weights")

# 2. Extract user weights
with zipfile.ZipFile(MODEL_PATH, 'r') as z:
    z.extract('model.weights.h5', '.')

# 3. Smart load loop
print("\nStarting smart weight loading...")
with h5py.File('model.weights.h5', 'r') as f:
    layers_grp = f['layers']
    
    # LOAD TOP LAYERS (Vital for classification)
    # We map user's layer names (e.g. 'dense_8') to our new names (e.g. 'dense')
    layer_map = {
        'batch_normalization': 'batch_normalization',
        'lstm': 'lstm',
        'dense': 'dense',
        'dense_1': 'dense_1'
    }
    
    # H5 file mapping keys (found from previous exploration)
    h5_keys = {
        'batch_normalization': 'batch_normalization',
        'lstm': 'lstm',
        'dense': 'dense',
        'dense_1': 'dense_1'
    }
    
    for my_name, h5_name in h5_keys.items():
        try:
            layer = model.get_layer(my_name)
            
            # Navigate h5 structure
            if h5_name == 'lstm':
                grp = layers_grp[h5_name]['cell']['vars']
                n_vars = 3
            else:
                grp = layers_grp[h5_name]['vars']
                n_vars = len(grp.keys())
                
            weights = [grp[str(i)][()] for i in range(n_vars)]
            
            # Check shapes
            current_shapes = [w.shape for w in layer.get_weights()]
            new_shapes = [w.shape for w in weights]
            
            if len(current_shapes) == len(new_shapes) and all(c==n for c,n in zip(current_shapes, new_shapes)):
                layer.set_weights(weights)
                print(f"✅ Loaded {my_name}")
            else:
                print(f"❌ Shape mismatch for {my_name}: {current_shapes} vs {new_shapes}")
                
        except Exception as e:
            print(f"⚠️ Could not load {my_name}: {e}")

    # LOAD EFFICIENTNET WEIGHTS (Where possible)
    print("\nAttempting to load EfficientNet weights...")
    td_layer = model.get_layer('time_distributed')
    inner_model = td_layer.layer
    
    # Corresponding group in h5
    try:
        eff_grp = layers_grp['time_distributed']['layer']['layers']
        
        loaded_count = 0
        skipped_count = 0
        
        for layer in inner_model.layers:
            # Try to find matching layer in h5
            if layer.name in eff_grp:
                l_grp = eff_grp[layer.name]
                if 'vars' in l_grp:
                   vars_grp = l_grp['vars']
                   n = len(vars_grp.keys())
                   if n > 0:
                       weights = [vars_grp[str(i)][()] for i in range(n)]
                       
                       # Verify shapes
                       try:
                           current_shapes = [w.shape for w in layer.get_weights()]
                           new_shapes = [w.shape for w in weights]
                           
                           if len(current_shapes) == len(new_shapes) and all(c==n for c,n in zip(current_shapes, new_shapes)):
                               layer.set_weights(weights)
                               loaded_count += 1
                           else:
                               # Keep ImageNet weights
                               skipped_count += 1
                       except:
                           skipped_count += 1
        
        print(f"Result: {loaded_count} layers loaded from user weights")
        print(f"        {skipped_count} layers kept as ImageNet (due to mismatch)")
        
    except Exception as e:
        print(f"EfficientNet loading issue: {e}")

os.remove('model.weights.h5')

# Test
print("\n=== VERIFICATION ===")
# Generate different inputs
zeros = np.zeros((1, SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3), dtype=np.float32)
ones = np.ones((1, SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3), dtype=np.float32)
rand = np.random.rand(1, SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3).astype(np.float32)

p_zeros = model.predict(zeros, verbose=0)
p_ones = model.predict(ones, verbose=0)
p_rand = model.predict(rand, verbose=0)

idx_z = np.argmax(p_zeros)
idx_o = np.argmax(p_ones)
idx_r = np.argmax(p_rand)

print(f"Zeros : Class {idx_z} ({p_zeros.max()*100:.1f}%)")
print(f"Ones  : Class {idx_o} ({p_ones.max()*100:.1f}%)")
print(f"Random: Class {idx_r} ({p_rand.max()*100:.1f}%)")

if idx_z == idx_o == idx_r:
    print("\n⚠️ WARNING: All inputs classified as same class!")
    print("This might be okay if inputs are garbage, but verify with real images.")
else:
    print("\n✅ SUCCESS: Different inputs produce different predictions!")

model.save('rebuilt_model_robust.keras')
print("Saved to rebuilt_model_robust.keras")
