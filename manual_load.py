"""
MANUAL weight loading approach - extract weights and load by layer position
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np
import keras
from keras import layers
from keras.applications import EfficientNetB0
import zipfile
import h5py

MODEL_PATH = "best_model_ultrafast.keras"

# Model specs
SEQUENCE_LENGTH = 10
IMG_SIZE = 112
NUM_CLASSES = 50

# Build model
print("Building model...")
inputs = layers.Input(shape=(SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3), name="input_layer_9")

base_model = EfficientNetB0(
    include_top=False,
    weights=None,
    pooling='avg',
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)
base_model.trainable = False

x = layers.TimeDistributed(base_model, name="time_distributed_4")(inputs)
x = layers.BatchNormalization(name="batch_normalization_4")(x)
x = layers.LSTM(64, return_sequences=False, name="lstm_5")(x)
x = layers.Dropout(0.4, name="dropout_9")(x)
x = layers.Dense(128, activation='relu', name="dense_8")(x)
x = layers.Dropout(0.4, name="dropout_10")(x)
outputs = layers.Dense(NUM_CLASSES, activation='softmax', name="dense_9")(x)

model = keras.Model(inputs=inputs, outputs=outputs, name="functional_4")
print(f"Model built: {model.input_shape} -> {model.output_shape}")

# Extract weights
print("\nExtracting weights from .keras file...")
with zipfile.ZipFile(MODEL_PATH, 'r') as z:
    z.extract('model.weights.h5', '.')

# Load weights manually by reading h5 file structure
print("Manually loading weights by iterating through layers...")

with h5py.File('model.weights.h5', 'r') as f:
    layers_group = f['layers']
    
    # Get all layer names from the weights file
    weight_layer_names = []
    
    def collect_names(name, obj):
        if 'vars' in name and isinstance(obj, h5py.Dataset):
            # Extract layer path
            parts = name.split('/')
            if len(parts) >= 2:
                layer_name = '/'.join(parts[:-2])  # Remove 'vars/0' part
                if layer_name not in weight_layer_names:
                    weight_layer_names.append(layer_name)
    
    layers_group.visititems(collect_names)
    print(f"Found {len(weight_layer_names)} unique layer paths with weights")
    
    # Now try loading specific important layers
    # BatchNormalization
    try:
        bn_layer = model.get_layer('batch_normalization_4')
        bn_weights_path = 'batch_normalization_4/vars'
        if bn_weights_path.replace('/vars', '') in str(layers_group.keys()):
            bn_group = layers_group['batch_normalization_4']['vars']
            weights = [bn_group[str(i)][()] for i in range(len(bn_group.keys()))]
            bn_layer.set_weights(weights)
            print("✅ BatchNormalization weights loaded")
    except Exception as e:
        print(f"❌ BatchNormalization: {e}")
    
    # LSTM
    try:
        lstm_layer = model.get_layer('lstm_5')
        lstm_group = layers_group['lstm_5']['cell']['vars']
        weights = [lstm_group[str(i)][()] for i in range(len(lstm_group.keys()))]
        lstm_layer.set_weights(weights[:3])  # kernel, recurrent_kernel, bias
        print("✅ LSTM weights loaded")
    except Exception as e:
        print(f"❌ LSTM: {e}")
    
    # Dense 8
    try:
        dense8 = model.get_layer('dense_8')
        d8_group = layers_group['dense_8']['vars']
        weights = [d8_group[str(i)][()] for i in range(len(d8_group.keys()))]
        dense8.set_weights(weights)
        print("✅ Dense8 weights loaded")
    except Exception as e:
        print(f"❌ Dense8: {e}")
    
    # Dense 9
    try:
        dense9 = model.get_layer('dense_9')
        d9_group = layers_group['dense_9']['vars']
        weights = [d9_group[str(i)][()] for i in range(len(d9_group.keys()))]
        dense9.set_weights(weights)
        print("✅ Dense9 weights loaded")
    except Exception as e:
        print(f"❌ Dense9: {e}")
    
    # TimeDistributed inner EfficientNet - this is more complex
    try:
        td_layer = model.get_layer('time_distributed_4')
        inner_model = td_layer.layer
        td_group = layers_group['time_distributed_4']['efficientnetb0']
        
        # Iterate through inner model layers
        loaded = 0
        for layer in inner_model.layers:
            if layer.name in td_group:
                layer_group = td_group[layer.name]
                if 'vars' in layer_group:
                    vars_group = layer_group['vars']
                    weights = [vars_group[str(i)][()] for i in range(len(vars_group.keys()))]
                    if len(weights) > 0:
                        try:
                            layer.set_weights(weights)
                            loaded += 1
                        except:
                            pass
        print(f"✅ EfficientNet inner layers loaded: {loaded} layers")
    except Exception as e:
        print(f"❌ TimeDistributed: {e}")

os.remove('model.weights.h5')

# Test predictions
print("\n=== Testing predictions ===")
for i, name in enumerate(['zeros', 'ones', 'random']):
    if name == 'zeros':
        test = np.zeros((1, SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3), dtype=np.float32)
    elif name == 'ones':
        test = np.ones((1, SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3), dtype=np.float32)
    else:
        test = np.random.rand(1, SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3).astype(np.float32)
    
    pred = model.predict(test, verbose=0)
    top_idx = np.argmax(pred)
    print(f"{name}: Top={top_idx}, Conf={pred[0][top_idx]*100:.2f}%")

# Save model
model.save('rebuilt_model_manual.keras')
print("\n✅ Model saved to rebuilt_model_manual.keras")
