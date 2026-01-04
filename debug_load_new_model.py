import os
import sys

# Add backend to path to potential import issues
sys.path.append(os.path.join(os.getcwd(), 'backend'))

MODEL_PATH = "final_model_fast_50_classes.keras"

print(f"Loading from: {MODEL_PATH}")
print(f"Exists: {os.path.exists(MODEL_PATH)}")

try:
    import keras
    print(f"Keras version: {keras.__version__}")
    
    model = keras.models.load_model(MODEL_PATH, compile=False)
    print("SUCCESS")
    print(model.summary())
except Exception as e:
    print("FAILED")
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
