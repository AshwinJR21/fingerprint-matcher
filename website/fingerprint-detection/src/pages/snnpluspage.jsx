import React, { useState } from 'react';
import axios from 'axios';

const Snnpluspage = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewImage, setPreviewImage] = useState(null); // For displaying the uploaded image
  const [resultImage, setResultImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(''); // To display the backend message like filename and score
  const[personDetails, setPersonDetails] =  useState([]);


  const handleImageChange = (event) => {
    const file = event.target.files[0];
    setSelectedImage(file);
    setPreviewImage(URL.createObjectURL(file)); // Show a preview of the uploaded image
    setResultImage(null); // Clear any previous result image
    setMessage(''); // Clear any previous message
    setPersonDetails('');
  };

  const handleSubmit = async () => {
    if (!selectedImage) return;

    // Set loading state to true
    setLoading(true);

    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const response = await axios.post('http://localhost:5000/snnplus-upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Set the result image and message (filename, score)
      setResultImage(`data:image/jpeg;base64,${response.data.processed_image}`);
      setMessage(`Score: ${response.data.score}`);
      setPersonDetails([`Name: ${response.data.name}`,
        `Gender: ${response.data.gender}`,
        `Hand: ${response.data.lr}`,
        `Finger: ${response.data.finger}`,
        `Date of Birth: ${response.data.dob}`,
        `Country: ${response.data.country}`,
        `Phone: ${response.data.phone}`,
        `Address: ${response.data.address}`])

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
    setPersonDetails('');
  };

  return (
    <div className="siftpage">
      <h1>Feature Comparison Fingerprint Matcher</h1>

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

      {personDetails && (
        <div>
          <ul><h2>Person Details</h2>
            <li>{personDetails[0]}</li>
            <li>{personDetails[1]}</li>
            <li>{personDetails[2]}</li>
            <li>{personDetails[3]}</li>
            <li>{personDetails[4]}</li>
            <li>{personDetails[5]}</li>
            <li>{personDetails[6]}</li>
            <li>{personDetails[7]}</li>
          </ul>
        </div>
      )}
    </div>
  );
};


export default Snnpluspage;
