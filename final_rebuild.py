"""
CORRECT MANUAL weight loading - use the proper layer name mapping from h5 file
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
SEQUENCE_LENGTH = 10
IMG_SIZE = 112
NUM_CLASSES = 50

# Build model
print("Building model...")
inputs = layers.Input(shape=(SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3), name="input_layer")

base_model = EfficientNetB0(
    include_top=False,
    weights=None,
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
print(f"Model built: {model.input_shape} -> {model.output_shape}")

# Extract weights
with zipfile.ZipFile(MODEL_PATH, 'r') as z:
    z.extract('model.weights.h5', '.')

print("\nLoading weights manually...")
loaded_layers = []
failed_layers = []

with h5py.File('model.weights.h5', 'r') as f:
    layers_grp = f['layers']
    
    # 1. BatchNormalization
    try:
        bn = model.get_layer('batch_normalization')
        bn_vars = layers_grp['batch_normalization']['vars']
        weights = [bn_vars[str(i)][()] for i in range(4)]
        bn.set_weights(weights)
        loaded_layers.append('batch_normalization')
    except Exception as e:
        failed_layers.append(f'batch_normalization: {e}')
    
    # 2. LSTM
    try:
        lstm = model.get_layer('lstm')
        lstm_vars = layers_grp['lstm']['cell']['vars']
        weights = [lstm_vars[str(i)][()] for i in range(3)]
        lstm.set_weights(weights)
        loaded_layers.append('lstm')
    except Exception as e:
        failed_layers.append(f'lstm: {e}')
    
    # 3. Dense (first one = relu)
    try:
        dense = model.get_layer('dense')
        dense_vars = layers_grp['dense']['vars']
        weights = [dense_vars[str(i)][()] for i in range(2)]
        dense.set_weights(weights)
        loaded_layers.append('dense')
    except Exception as e:
        failed_layers.append(f'dense: {e}')
    
    # 4. Dense_1 (output softmax)
    try:
        dense1 = model.get_layer('dense_1')
        dense1_vars = layers_grp['dense_1']['vars']
        weights = [dense1_vars[str(i)][()] for i in range(2)]
        dense1.set_weights(weights)
        loaded_layers.append('dense_1')
    except Exception as e:
        failed_layers.append(f'dense_1: {e}')
    
    # 5. TimeDistributed inner EfficientNet
    try:
        td = model.get_layer('time_distributed')
        inner = td.layer
        td_layers = layers_grp['time_distributed']['layer']['layers']
        
        loaded_inner = 0
        for layer in inner.layers:
            if layer.name in td_layers:
                layer_grp = td_layers[layer.name]
                if 'vars' in layer_grp:
                    vars_grp = layer_grp['vars']
                    n_vars = len(vars_grp.keys())
                    if n_vars > 0:
                        weights = [vars_grp[str(i)][()] for i in range(n_vars)]
                        try:
                            layer.set_weights(weights)
                            loaded_inner += 1
                        except:
                            pass
        loaded_layers.append(f'time_distributed ({loaded_inner} inner layers)')
    except Exception as e:
        failed_layers.append(f'time_distributed: {e}')

print(f"\n✅ Loaded: {loaded_layers}")
print(f"❌ Failed: {failed_layers}")

os.remove('model.weights.h5')

# Test predictions
print("\n=== Testing predictions ===")
for name, test_type in [('zeros', 0), ('ones', 1), ('random', 2)]:
    if test_type == 0:
        test = np.zeros((1, SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3), dtype=np.float32)
    elif test_type == 1:
        test = np.ones((1, SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3), dtype=np.float32)
    else:
        np.random.seed(42)
        test = np.random.rand(1, SEQUENCE_LENGTH, IMG_SIZE, IMG_SIZE, 3).astype(np.float32)
    
    pred = model.predict(test, verbose=0)
    top_idx = np.argmax(pred)
    top5 = np.argsort(pred[0])[-5:][::-1]
    print(f"{name}: Top={top_idx} ({pred[0][top_idx]*100:.1f}%), Top5={top5}")

# Save
model.save('rebuilt_model_final.keras')
print("\n✅ Model saved to rebuilt_model_final.keras")
