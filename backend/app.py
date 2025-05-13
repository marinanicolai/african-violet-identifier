from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import tensorflow as tf
import io

app = Flask(__name__)
CORS(app)


# Mock the model's behavior
class MockModel:
    def predict(self, img_array):
        # Return a mock prediction (e.g., class_id=1 with confidence=0.95)
        return [[0.05, 0.95]]

# Use the mock model instead of loading the actual model
model = MockModel()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        file = request.files['image']
        if not file.content_type.startswith('image/'):
            return jsonify({'error': 'Uploaded file is not an image'}), 400

        img = Image.open(io.BytesIO(file.read())).resize((224, 224))
        img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

        prediction = model.predict(img_array)
        predicted_class = int(np.argmax(prediction))

        return jsonify({'class_id': predicted_class, 'confidence': float(np.max(prediction))})
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return jsonify({'error': 'An error occurred during prediction'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True)
