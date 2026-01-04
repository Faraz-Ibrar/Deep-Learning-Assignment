"""
Test loading model weights only (without full model architecture)
"""
import os
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Reduce TF logging

import tensorflow as tf
print(f"TensorFlow version: {tf.__version__}")

MODEL_PATH = "best_model_ultrafast.keras"

# Try loading with tf_keras first
try:
    print("\nAttempting to load with tf_keras...")
    import tf_keras
    model = tf_keras.models.load_model(MODEL_PATH, compile=False)
    print("SUCCESS with tf_keras!")
    print(f"Input shape: {model.input_shape}")
    print(f"Output shape: {model.output_shape}")
    
    # Test prediction
    test_input = np.random.rand(1, 10, 112, 112, 3).astype(np.float32)
    print(f"\nTest input shape: {test_input.shape}")
    pred = model.predict(test_input, verbose=0)
    print(f"Prediction shape: {pred.shape}")
    print(f"Top 5 predictions: {np.argsort(pred[0])[-5:][::-1]}")
    
except Exception as e:
    print(f"tf_keras failed: {e}")
    
    # Try keras
    try:
        print("\nAttempting to load with keras...")
        import keras
        model = keras.models.load_model(MODEL_PATH, compile=False)
        print("SUCCESS with keras!")
        print(f"Input shape: {model.input_shape}")
        print(f"Output shape: {model.output_shape}")
    except Exception as e2:
        print(f"keras failed: {e2}")
        
        # Try tf.keras
        try:
            print("\nAttempting to load with tf.keras...")
            model = tf.keras.models.load_model(MODEL_PATH, compile=False)
            print("SUCCESS with tf.keras!")
            print(f"Input shape: {model.input_shape}")
            print(f"Output shape: {model.output_shape}")
        except Exception as e3:
            print(f"tf.keras failed: {e3}")
            print("\nAll loading methods failed!")
