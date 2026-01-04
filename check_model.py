"""
Detailed model inspection
"""
import zipfile
import json

# Read model config
z = zipfile.ZipFile('best_model_ultrafast.keras')
c = json.loads(z.read('config.json'))

# Print metadata
print("=== METADATA ===")
m = json.loads(z.read('metadata.json'))
print(json.dumps(m, indent=2))

# Print model class
print("\n=== MODEL CLASS ===")
print(f"Class: {c.get('class_name')}")
print(f"Name: {c.get('config', {}).get('name')}")

# Print input layer details
print("\n=== INPUT LAYER ===")
layers = c.get('config', {}).get('layers', [])
input_layer = layers[0] if layers else {}
print(f"Input layer class: {input_layer.get('class_name')}")
print(f"Input layer config: {json.dumps(input_layer.get('config', {}), indent=2)}")

# Print TimeDistributed layer details  
print("\n=== TIMEDISTRIBUTED LAYER ===")
td_layer = layers[1] if len(layers) > 1 else {}
print(f"TimeDistributed class: {td_layer.get('class_name')}")

# Get inner layer config
inner_layer = td_layer.get('config', {}).get('layer', {})
print(f"Inner layer class: {inner_layer.get('class_name')}")
print(f"Inner layer name: {inner_layer.get('config', {}).get('name')}")

# Check build_config
build_config = td_layer.get('build_config', {})
print(f"Build config: {build_config}")

print("\n=== FILES IN MODEL ===")
print(z.namelist())
