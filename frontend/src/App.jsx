import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth0 } from '@auth0/auth0-react';
import { FILES_ENDPOINT, OPERATIONS_ENDPOINT, USER_ENDPOINT } from './constants/APIConstants';

const App = () => {
    const { loginWithRedirect, logout, user, isAuthenticated, isLoading, getAccessTokenSilently } = useAuth0();
    const [operations, setOperations] = useState({});
    const [files, setFiles] = useState([]);
    const [uploadFile, setUploadFile] = useState(null);
    const [message, setMessage] = useState('');

    useEffect(() => {
        if (isAuthenticated) {
            createUser(); // Create or fetch user when authenticated
            fetchOperations();
            fetchFiles();
        }
    }, [isAuthenticated]);

    const createUser = async () => {
        try {
            const token = await getAccessTokenSilently();
            // Use the part before "@" symbol as username
            const username = user.email.split('@')[0]; 

            const response = await axios.post(USER_ENDPOINT, {
                username: username,
                email: user.email,
            }, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            localStorage.setItem('token', response.data.token); // Store the token if needed
        } catch (error) {
            console.error('Error creating user:', error);
        }
    };

    const fetchOperations = async () => {
        try {
            const token = await getAccessTokenSilently();
            const response = await axios.get(`${OPERATIONS_ENDPOINT}?token=${localStorage.getItem('token')}`, {
                headers: {
                    accept: 'application/json',
                },
            });
            setOperations(response.data);
        } catch (error) {
            console.error('Error fetching operations:', error.response ? error.response.data : error);
            setMessage('Failed to fetch operations.');
        }
    };

    const fetchFiles = async () => {
        try {
            const token = await getAccessTokenSilently();
            const response = await axios.get(`${FILES_ENDPOINT}?token=${localStorage.getItem('token')}`, {
                headers: {
                    accept: 'application/json',
                },
            });
            setFiles(response.data);
        } catch (error) {
            console.error('Error fetching files:', error);
        }
    };

    const handleFileUpload = async () => {
        const formData = new FormData();
        formData.append('file', uploadFile);

        try {
            const token = await getAccessTokenSilently();
            await axios.post(`${FILES_ENDPOINT}?token=${localStorage.getItem('token')}`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    accept: 'application/json',
                },
            });
            setMessage('File uploaded successfully!');
            setUploadFile(null); // Reset the file input
            fetchFiles(); // Re-fetch files to include the newly uploaded file
            fetchOperations(); // Re-fetch operations to update the count
        } catch (error) {
            console.error('Error uploading file:', error);
            setMessage('Failed to upload file.');
        }
    };

    const handleFileDelete = async (fileId) => {
        try {
            const token = await getAccessTokenSilently();
            await axios.delete(`${FILES_ENDPOINT}/${fileId}?token=${localStorage.getItem('token')}`, {
                headers: {
                    accept: 'application/json',
                },
            });
            setMessage('File deleted successfully!');
            fetchFiles(); // Re-fetch files
            fetchOperations(); // Re-fetch operations
        } catch (error) {
            console.error('Error deleting file:', error);
            setMessage('Failed to delete file.');
        }
    };

    const handleFileDownload = async (fileUrl, fileId) => {
        try {
            // Trigger the file download without redirecting the page
            const token = localStorage.getItem('token');
            const downloadUrl = `${fileUrl}/?token=${token}`;

            // Create an anchor element and trigger a click event to download the file
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = ''; // Optionally, you can specify a filename here
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);

            // After initiating the download, update the operations count
            fetchOperations(); // Re-fetch operations after download
        } catch (error) {
            console.error('Error downloading file:', error);
        }
    };

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (!isAuthenticated) {
        return (
            <div style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100vh',
                width: '100vw',
            }}>
                <button onClick={loginWithRedirect}>Login</button>
            </div>
        );
    }

    return (
        <div style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            height: '100vh',
            width: '100vw',
        }}>
            <div style={{
                textAlign: 'center',
                padding: '20px',
                border: '1px solid #ccc',
                borderRadius: '8px',
                width: '400px',
                boxShadow: '0 4px 10px rgba(0,0,0,0.1)',
            }}>
                <h1>One Project</h1>
                <div>
                    <h2>Welcome, {user.name}</h2>
                    <button onClick={() => logout({ returnTo: window.location.origin })}>
                        Logout
                    </button>
                </div>

                <h2>Operations Count</h2>
                <table style={{ margin: '0 auto', borderCollapse: 'collapse' }}>
                    <tbody>
                        <tr>
                            <td style={{ padding: '20px', border: '1px solid black', fontSize: '1.5em' }}>Downloads:</td>
                            <td style={{ padding: '20px', border: '1px solid black', fontSize: '1.5em' }}>{operations.download || 0}</td>
                        </tr>
                        <tr>
                            <td style={{ padding: '20px', border: '1px solid black', fontSize: '1.5em' }}>Deletes:</td>
                            <td style={{ padding: '20px', border: '1px solid black', fontSize: '1.5em' }}>{operations.delete || 0}</td>
                        </tr>
                        <tr>
                            <td style={{ padding: '20px', border: '1px solid black', fontSize: '1.5em' }}>Uploads:</td>
                            <td style={{ padding: '20px', border: '1px solid black', fontSize: '1.5em' }}>{operations.upload || 0}</td>
                        </tr>
                    </tbody>
                </table>

                <h2>Files</h2>
                <ul style={{ listStyleType: 'none', padding: 0 }}>
                    {files.map(file => (
                        <li key={file.file_id}>
                            <span>{file.name}</span>
                            <button onClick={() => handleFileDownload(file.url, file.file_id)}>Download</button>
                            <button onClick={() => handleFileDelete(file.file_id)}>Delete</button>
                        </li>
                    ))}
                </ul>

                <h2>Upload New File</h2>
                <input 
                    type="file" 
                    onChange={e => setUploadFile(e.target.files[0])} 
                    key={uploadFile ? uploadFile.name : ''} // Reset file input after upload
                />
                <button onClick={handleFileUpload}>Upload</button>

                {message && <p>{message}</p>}
            </div>
        </div>
    );
};

export default App;
