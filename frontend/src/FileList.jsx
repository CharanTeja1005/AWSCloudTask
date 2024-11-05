import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FILES_ENDPOINT } from './constants/APIConstants';

const FileList = ({ fetchOperations }) => {
    const [files, setFiles] = useState([]);

    const fetchFiles = async (getAccessTokenSilently) => {
        try {
            const token = await getAccessTokenSilently();
            const response = await axios.get(FILES_ENDPOINT, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setFiles(response.data);
        } catch (error) {
            console.error('Error fetching files:', error);
        }
    };

    const handleFileDelete = async (fileId, getAccessTokenSilently) => {
        try {
            const token = await getAccessTokenSilently();
            await axios.delete(`${FILES_ENDPOINT}/${fileId}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            fetchFiles();
            fetchOperations();
        } catch (error) {
            console.error('Error deleting file:', error);
        }
    };

    useEffect(() => {
        fetchFiles();
    }, []);

    return (
        <div>
            <h2>Files</h2>
            <ul>
                {files.map(file => (
                    <li key={file.file_id}>
                        {file.name}
                        <button onClick={() => handleFileDownload(file.url)}>Download</button>
                        <button onClick={() => handleFileDelete(file.file_id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default FileList;
