import React, { useState } from 'react';
import axios from 'axios';
import { FILES_ENDPOINT } from './constants/APIConstants';

const FileUpload = () => {
    const [uploadFile, setUploadFile] = useState(null);
    const [message, setMessage] = useState('');

    const handleFileUpload = async (getAccessTokenSilently) => {
        const formData = new FormData();
        formData.append('file', uploadFile);

        try {
            const token = await getAccessTokenSilently();
            await axios.post(FILES_ENDPOINT, formData, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setMessage('File uploaded successfully!');
            setUploadFile(null);
        } catch (error) {
            console.error('Error uploading file:', error);
            setMessage('Failed to upload file.');
        }
    };

    return (
        <div>
            <h2>Upload New File</h2>
            <input type="file" onChange={(e) => setUploadFile(e.target.files[0])} />
            <button onClick={() => handleFileUpload()}>Upload</button>
            {message && <p>{message}</p>}
        </div>
    );
};

export default FileUpload;
