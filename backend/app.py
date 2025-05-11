from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import tensorflow as tf
import io

app = Flask(__name__)
CORS(app)

# Load your trained model here (replace with your actual model path)
model = tf.keras.models.load_model('model/violet_model.h5')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    img = Image.open(io.BytesIO(file.read())).resize((224, 224))
    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

    prediction = model.predict(img_array)
    predicted_class = int(np.argmax(prediction))

    return jsonify({'class_id': predicted_class, 'confidence': float(np.max(prediction))})

if __name__ == '__main__':
    app.run(debug=True)
