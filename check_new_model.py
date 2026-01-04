import zipfile
import json
import os

MODEL_PATH = "final_model_fast_50_classes.keras"
print(f"Checking {MODEL_PATH}...")

try:
    with zipfile.ZipFile(MODEL_PATH, 'r') as z:
        c = json.loads(z.read('config.json'))

    layers = c.get('config', {}).get('layers', [])
    print(f"Input shape: {layers[0]['config']['batch_shape']}")
    
    # Check what is inside TimeDistributed
    td = layers[1]
    print(f"Layer 1: {td['class_name']}")
    if td['class_name'] == 'TimeDistributed':
        inner = td['config']['layer']
        print(f"Inner name: {inner['class_name']}")
        print(f"Inner config name: {inner['config']['name']}")

except Exception as e:
    print(f"Error: {e}")
