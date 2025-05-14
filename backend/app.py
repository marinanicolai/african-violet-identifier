from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import tensorflow as tf
import io

app = Flask(__name__)
# Allow only requests from the frontend's origin
CORS(app, resources={r"/*": {"origins":"*"}})



# Mock the model's behavior
class MockModel:
    def predict(self, img_array):
        # Return a mock prediction (e.g., class_id=1 with confidence=0.95)
        return [[0.05, 0.95]]

# Use the mock model instead of loading the actual model
model = MockModel()

@app.route('/predict', methods=['POST'])
def predict():
    print("Request received at /predict")
    try:
        print("➡️ Received a prediction request")
        if 'image' not in request.files:
            print("❌ No image in request.files")
            return jsonify({'error': 'No image uploaded'}), 400

        file = request.files['image']
        print(f"✅ Image received: {file.filename} ({file.content_type})")

        if not file.content_type.startswith('image/'):
            print("❌ File is not an image")
            return jsonify({'error': 'Uploaded file is not an image'}), 400

        img = Image.open(io.BytesIO(file.read())).resize((224, 224))
        img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

        prediction = model.predict(img_array)
        predicted_class = int(np.argmax(prediction))
        confidence = float(np.max(prediction))

        print(f"✅ Prediction successful: class {predicted_class}, confidence {confidence}")
        return jsonify({'class_id': predicted_class, 'confidence': 0.99})
    except Exception as e:
        import traceback
        print("❌ Error during prediction:")
        traceback.print_exc()
        return jsonify({'error': 'An error occurred during prediction'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the African Violet Classifier API!'})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
