import React, { useState } from 'react';
import axios from 'axios';

const SnnPage = () => {
  const [image1, setImage1] = useState(null);
  const [image2, setImage2] = useState(null);
  const [previewImage1, setPreviewImage1] = useState(null);
  const [previewImage2, setPreviewImage2] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleImage1Change = (event) => {
    const file = event.target.files[0];
    setImage1(file);
    setPreviewImage1(URL.createObjectURL(file));
  };

  const handleImage2Change = (event) => {
    const file = event.target.files[0];
    setImage2(file);
    setPreviewImage2(URL.createObjectURL(file));
  };

  const handleSubmit = async () => {
    if (!image1 || !image2) {
      alert("Please upload both images.");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append('image1', image1);
    formData.append('image2', image2);

    try {
      const response = await axios.post('http://localhost:5000/process_snn', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(`data:image/jpeg;base64,${response.data.result_image}`);
      setMessage(`Score: ${response.data.score}`);
    } catch (error) {
      console.error('Error processing the images:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setImage1(null);
    setImage2(null);
    setPreviewImage1(null);
    setPreviewImage2(null);
    setResult(null);
    setMessage('');
    setLoading(false);
  };

  return (
    <div className="snnpage">
      <h1>Siamese Neural Network Matcher</h1>

      <input type="file" onChange={handleImage1Change} accept="image/*" />
      {previewImage1 && <img src={previewImage1} alt="Preview 1" style={{ width: '250px' }} />}

      <input type="file" onChange={handleImage2Change} accept="image/*" />
      {previewImage2 && <img src={previewImage2} alt="Preview 2" style={{ width: '250px' }} />}

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Processing...' : 'Process Images'}
      </button>
      <button onClick={handleClear}>Clear</button>

      {loading && (
        <div className="loading-dots">
          <span>.</span><span>.</span><span>.</span>
        </div>
      )}

      {result && (
        <div>
          <h2>Result Image</h2>
          <img src={result} alt="Result" style={{ width: '500px' }} />
        </div>
      )}

      {message && <p>{message}</p>}
    </div>
  );
};

export default SnnPage;
