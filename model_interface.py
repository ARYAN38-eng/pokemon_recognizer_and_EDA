import cv2
import os
import numpy as np
import tensorflow as tf 

# Load the model
model_path = os.path.join(os.path.dirname(__file__), 'model', 'best_model.keras')
model = tf.keras.models.load_model(model_path)

def predict_image(file):
    # Read and decode the image
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # Resize the image to 150x150
    img = cv2.resize(img, (150, 150))
    
    # Normalize the image
    img_normalized = img / 255.0
    
    # Expand dimensions to create a batch
    img_batch = np.expand_dims(img_normalized, axis=0)
    
    # Predict
    prediction = model.predict(img_batch)
    final_pred = np.argmax(prediction, axis=1)
    
    # Return the corresponding Pokémon name
    if final_pred == 0:
        return "Name: Pikachu, Type 1: Electric, Type 2: 0, Total: 320, HP: 35, Attack: 55, Defense: 40, Special Attack: 50, Special Defence: 50, Speed: 90"
    elif final_pred == 1:
        return "Name: Bulbasaur, Type 1: Grass, Type 2: Poison, Total: 318, HP: 45, Attack: 49, Defense: 49, Special Attack: 65, Special Defence: 65, Speed: 45"
    elif final_pred == 2:
        return "Name: Ditto, Type 1: Normal, Type 2: 0, Total: 288, HP: 48, Attack: 48, Defense: 48, Special Attack: 48, Special Defence: 48, Speed: 48"
    else:
        return "Name: Magmar, Type 1: Fire, Type 2: 0, Total: 495, HP: 65, Attack: 95, Defense: 57, Special Attack: 100, Special Defence: 85, Speed: 93"
