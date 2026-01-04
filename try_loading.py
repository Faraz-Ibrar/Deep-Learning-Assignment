"""
Try different approaches to make the original model work
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np

# Try 1: Use tf_keras which has Keras 2 compatible API
print("=" * 60)
print("ATTEMPT 1: Try loading with tf_keras (Keras 2 compatible)")
print("=" * 60)
try:
    import tf_keras
    model = tf_keras.models.load_model(
        'best_model_ultrafast.keras',
        compile=False
    )
    print("SUCCESS! Model loaded with tf_keras")
    print(f"Input shape: {model.input_shape}")
    print(f"Output shape: {model.output_shape}")
    
    # Test
    test_input = np.random.rand(1, 10, 112, 112, 3).astype(np.float32)
    pred = model.predict(test_input, verbose=0)
    print(f"Test prediction - Top class: {np.argmax(pred)}, confidence: {pred.max()*100:.2f}%")
    
    # Save with tf_keras
    model.save('model_tf_keras.keras')
    print("Saved to model_tf_keras.keras")
    
except Exception as e:
    print(f"FAILED: {e}")

# Try 2: Try loading as SavedModel format
print("\n" + "=" * 60)
print("ATTEMPT 2: Try converting to SavedModel format")
print("=" * 60)
try:
    import tensorflow as tf
    import zipfile
    import shutil
    
    # Extract the .keras file 
    with zipfile.ZipFile('best_model_ultrafast.keras', 'r') as z:
        print("Files in .keras:", z.namelist())
        
except Exception as e:
    print(f"FAILED: {e}")

# Try 3: Set Keras to use legacy format
print("\n" + "=" * 60)
print("ATTEMPT 3: Try with keras legacy mode")
print("=" * 60)
try:
    import keras
    # Check keras version
    print(f"Keras version: {keras.__version__}")
    
    # Try loading with different settings
    model = keras.saving.load_model(
        'best_model_ultrafast.keras',
        compile=False,
        safe_mode=False
    )
    print("SUCCESS!")
except Exception as e:
    print(f"FAILED: {e}")
