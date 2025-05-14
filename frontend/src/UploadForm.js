import axios from 'axios';
import { useState } from 'react';

function UploadForm() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    setImage(e.target.files[0]);
    console.log('Selected file:', e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!image) {
      alert('Please choose an image first.');
      return;
    }

    const formData = new FormData();
    formData.append('image', image);

    console.log('Uploading to:', 'http://localhost:5000/predict');
    console.log('FormData:', formData);

    try {
      const response = await axios.post('http://localhost:5001/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        // Add withCredentials if you want to debug cookies/CORS
        // withCredentials: true,
      });
      console.log('Prediction result:', response.data);
      setResult(response.data); 
    } catch (error) {
      console.error('Prediction error:', error);
      if (error.response) {
        // The request was made and the server responded with a status code
        console.error('Response data:', error.response.data);
        console.error('Response status:', error.response.status);
        console.error('Response headers:', error.response.headers);
      } else if (error.request) {
        // The request was made but no response was received
        console.error('No response received:', error.request);
      } else {
        // Something happened in setting up the request
        console.error('Error setting up request:', error.message);
      }
      alert('An error occurred while making the prediction.');
    }
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload & Predict</button>

      {result && (
        <div>
          <p>Class ID: {result.class_id}</p>
          <p>Confidence: {result.confidence}</p>
        </div>
      )}
    </div>
  );
}

export default UploadForm;