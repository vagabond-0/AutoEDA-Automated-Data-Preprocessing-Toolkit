// components/FileUpload.jsx
import React from 'react';
import './styles.css'; // Import the CSS file for styling

const FileUpload = () => {
  return (
    <div className="file-upload-container">
      <h2>Upload Your CSV File</h2>
      <p>Please select a CSV file to upload for preprocessing:</p>
      <input type="file" accept=".csv" className="file-input" />
      <button className="upload-button">Upload</button>
    </div>
  );
};

export default FileUpload;
