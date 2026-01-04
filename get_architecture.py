"""
Get exact model architecture from config.json
"""
import zipfile
import json

MODEL_PATH = "best_model_ultrafast.keras"

# Read model config
with zipfile.ZipFile(MODEL_PATH, 'r') as z:
    c = json.loads(z.read('config.json'))

# Print all layers with their configurations
layers = c.get('config', {}).get('layers', [])
print(f"Total layers: {len(layers)}\n")

for i, layer in enumerate(layers):
    class_name = layer.get('class_name', 'Unknown')
    name = layer.get('config', {}).get('name', 'Unknown')
    print(f"Layer {i}: {class_name} ({name})")
    
    config = layer.get('config', {})
    
    # Print relevant config for each layer type
    if class_name == 'LSTM':
        print(f"  - units: {config.get('units')}")
        print(f"  - return_sequences: {config.get('return_sequences')}")
    elif class_name == 'Dense':
        print(f"  - units: {config.get('units')}")
        print(f"  - activation: {config.get('activation')}")
    elif class_name == 'Dropout':
        print(f"  - rate: {config.get('rate')}")
    elif class_name == 'InputLayer':
        print(f"  - batch_shape: {config.get('batch_shape')}")
    elif class_name == 'TimeDistributed':
        inner = config.get('layer', {})
        print(f"  - inner class: {inner.get('class_name')}")
        print(f"  - inner name: {inner.get('config', {}).get('name')}")
    
    print()
