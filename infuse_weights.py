"""
Infuse ImageNet weights into the rebuilt model
This fixes the 'feature extractor is dead' issue
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import keras
from keras.applications import EfficientNetB0

MODEL_PATH = "rebuilt_model_correct.keras"

print("Loading rebuilt model...")
model = keras.models.load_model(MODEL_PATH)
print("Model loaded.")

print("Loading ImageNet weights...")
# Create dummy model just to download/load ImageNet weights
imagenet_model = EfficientNetB0(
    include_top=False,
    weights='imagenet',
    pooling='avg',
    input_shape=(112, 112, 3)
)
imagenet_weights = imagenet_model.get_weights()
print(f"Got {len(imagenet_weights)} weight tensors from ImageNet")

print("Injecting weights into TimeDistributed backbone...")
td_layer = model.get_layer('time_distributed_4')
inner_model = td_layer.layer

# Verify shapes match before setting
current_weights = inner_model.get_weights()
print(f"Target model expects {len(current_weights)} weight tensors")

if len(current_weights) == len(imagenet_weights):
    print("Layer count matches!")
    inner_model.set_weights(imagenet_weights)
    print("✅ ImageNet weights infused successfully!")
else:
    print(f"❌ Layer count mismatch! {len(current_weights)} vs {len(imagenet_weights)}")
    # Try creating it with exactly matching config if mismatch

# Test predictions
print("\n=== VERIFICATION ===")
zeros = np.zeros((1, 10, 112, 112, 3), dtype=np.float32)
ones = np.ones((1, 10, 112, 112, 3), dtype=np.float32)
rand = np.random.rand(1, 10, 112, 112, 3).astype(np.float32)

p_zeros = model.predict(zeros, verbose=0)
p_ones = model.predict(ones, verbose=0)
p_rand = model.predict(rand, verbose=0)

idx_z = np.argmax(p_zeros)
idx_o = np.argmax(p_ones)
idx_r = np.argmax(p_rand)

print(f"Zeros : Top={idx_z} ({p_zeros.max()*100:.1f}%)")
print(f"Ones  : Top={idx_o} ({p_ones.max()*100:.1f}%)")
print(f"Random: Top={idx_r} ({p_rand.max()*100:.1f}%)")

if idx_z != idx_o or idx_z != idx_r:
    print("\n✅ SUCCESS: Predictions vary by input!")
else:
    print("\n⚠️ WARNING: Still same predictions?")

model.save('rebuilt_model_final_fixed.keras')
print("Saved to rebuilt_model_final_fixed.keras")
