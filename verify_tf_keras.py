"""
Verify tf_keras loading AND prediction
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np
import tf_keras as keras  # Use legacy Keras 2
import tensorflow as tf

print(f"Using tf_keras version: {keras.__version__}")

MODEL_PATH = "best_model_ultrafast.keras"

try:
    print("Loading with tf_keras...")
    model = keras.models.load_model(MODEL_PATH, compile=False)
    print("SUCCESS! Model loaded.")
    
    # Test prediction
    print("Testing prediction...")
    # Zeros
    zeros = np.zeros((1, 10, 112, 112, 3), dtype=np.float32)
    pred_0 = model.predict(zeros, verbose=0)
    print(f"Zeros: Top={np.argmax(pred_0)} ({pred_0.max()*100:.2f}%)")
    
    # Random
    np.random.seed(42)
    rand = np.random.rand(1, 10, 112, 112, 3).astype(np.float32)
    pred_r = model.predict(rand, verbose=0)
    print(f"Random: Top={np.argmax(pred_r)} ({pred_r.max()*100:.2f}%)")
    
    if np.argmax(pred_0) != np.argmax(pred_r):
        print("✅ Predictions vary! Model is working.")
    else:
        print("⚠️ Predictions is same. Check confidence.")
        print(f"Zeros conf: {pred_0[0][:5]}")
        print(f"Rand conf: {pred_r[0][:5]}")

except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
