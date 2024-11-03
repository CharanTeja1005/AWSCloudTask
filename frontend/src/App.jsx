import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth0 } from '@auth0/auth0-react';

const App = () => {
    const { loginWithRedirect, logout, user, isAuthenticated, isLoading } = useAuth0();
    const [operations, setOperations] = useState({});
    const [files, setFiles] = useState([]);
    const [uploadFile, setUploadFile] = useState(null);
    const [message, setMessage] = useState('');

    // Fetch operations and files on component mount
    useEffect(() => {
        if (isAuthenticated) {
            fetchOperations();
            fetchFiles();
        }
    }, [isAuthenticated]); // Run when authentication status changes

    const fetchOperations = async () => {
        try {
            const response = await axios.get('http://localhost:8000/operations');
            setOperations(response.data);
        } catch (error) {
            console.error('Error fetching operations:', error);
        }
    };

    const fetchFiles = async () => {
        try {
            const response = await axios.get('http://localhost:8000/files');
            setFiles(response.data);
        } catch (error) {
            console.error('Error fetching files:', error);
        }
    };

    const handleFileUpload = async () => {
        const formData = new FormData();
        formData.append('file', uploadFile);

        try {
            await axios.post('http://localhost:8000/files', formData);
            setMessage('File uploaded successfully!');
            setUploadFile(null); // Clear the file input
            fetchFiles(); // Refresh files
            fetchOperations(); // Refresh operations
        } catch (error) {
            console.error('Error uploading file:', error);
            setMessage('Failed to upload file.');
        }
    };

    const handleFileDelete = async (fileId) => {
        try {
            await axios.delete(`http://localhost:8000/files/${fileId}`);
            setMessage('File deleted successfully!');
            fetchFiles(); // Refresh files
            fetchOperations(); // Refresh operations
        } catch (error) {
            console.error('Error deleting file:', error);
            setMessage('Failed to delete file.');
        }
    };

    const handleFileDownload = (fileUrl) => {
        window.open(fileUrl, '_blank');
        fetchOperations(); // Refresh operations after downloading
    };

    // Render loading state if the Auth0 is loading
    if (isLoading) {
        return <div>Loading...</div>;
    }

    // Render the application only if the user is authenticated
    if (!isAuthenticated) {
        return (
            <div style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100vh',
                width: '100vw',
                position: 'relative'
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
            position: 'relative'
        }}>
            <div style={{
                textAlign: 'center',
                padding: '20px',
                border: '1px solid #ccc',
                borderRadius: '8px',
                width: '400px',
                boxShadow: '0 4px 10px rgba(0,0,0,0.1)'
            }}>
                <h1>File Operations</h1>
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
                            <button onClick={() => handleFileDownload(file.url)}>Download</button>
                            <button onClick={() => handleFileDelete(file.file_id)}>Delete</button>
                        </li>
                    ))}
                </ul>

                <h2>Upload New File</h2>
                <input 
                    type="file" 
                    onChange={e => setUploadFile(e.target.files[0])} 
                />
                <button onClick={handleFileUpload}>Upload</button>

                {message && <p>{message}</p>}
            </div>
        </div>
    );
};

export default App;
