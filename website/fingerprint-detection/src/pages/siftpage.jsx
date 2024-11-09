import React, { useState } from 'react';
import axios from 'axios';

const Siftpage = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewImage, setPreviewImage] = useState(null); // For displaying the uploaded image
  const [resultImage, setResultImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(''); // To display the backend message like filename and score

  const handleImageChange = (event) => {
    const file = event.target.files[0];
    setSelectedImage(file);
    setPreviewImage(URL.createObjectURL(file)); // Show a preview of the uploaded image
    setResultImage(null); // Clear any previous result image
    setMessage(''); // Clear any previous message
  };

  const handleSubmit = async () => {
    if (!selectedImage) return;

    // Set loading state to true
    setLoading(true);

    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const response = await axios.post('http://localhost:5000/sift-upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Set the result image and message (filename, score)
      setResultImage(`data:image/jpeg;base64,${response.data.processed_image}`);
      setMessage(`Matched file: ${response.data.filename}, Score: ${response.data.score}`);

    } catch (error) {
      console.error('Error processing the image:', error);
    } finally {
      // Set loading state back to false
      setLoading(false);
    }
  };

  const handleClear = () => {
    setSelectedImage(null);
    setPreviewImage(null);
    setResultImage(null);
    setMessage('');
    setLoading(false);
  };

  return (
    <div className="siftpage">
      <h1>Fingerprint Matcher</h1>

      {/* Image upload input */}
      <input type="file" onChange={handleImageChange} accept="image/*" />

      {/* Show uploaded image preview */}
      {previewImage && (
        <div>
          <h3>Uploaded Image:</h3>
          <img src={previewImage} alt="Uploaded preview" style={{ width: '250px' }} />
        </div>
      )}
      
      {/* Submit button */}
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Processing...' : 'Process Image'}
      </button>

      {/* Clear button */}
      <button onClick={handleClear}>
        Clear
      </button>

      {/* Display loading animation */}
      {loading && (
        <div className="loading-dots">
          <span>.</span><span>.</span><span>.</span>
        </div>
      )}

      {/* Display the processed result image */}
      {resultImage && (
        <div>
          <h2>Processed Image</h2>
          <img src={resultImage} alt="Processed result" style={{ width: '500px' }} />
        </div>
      )}

      {/* Display backend message (filename and score) */}
      {message && <p>{message}</p>}
    </div>
  );
};

export default Siftpage;