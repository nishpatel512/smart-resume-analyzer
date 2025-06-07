import React, { useState } from 'react';
import axios from 'axios';

function UploadForm({ onUploadSuccess }){
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => setFile(e.target.files[0]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) return;

        //Declare formData before using
        const formData = new FormData();
        //FormData is a special object used to send files.
        formData.append('file', file);
        
        //sends file to FastAPI and calls the parent components onUploadSuccess with response
        try {
            const res = await axios.post('http://localhost:8000/upload-resume/', formData);
            alert('Upload successful!');
            onUploadSuccess(res.data); // resume_id must be present for this to work
        } catch (error) {
            console.error(error);
            alert('Upload failed!');
        }
    };


    return (
        <form onSubmit={handleSubmit}>
            <input type='file' onChange={handleFileChange}/>
            <button type='submit'>Upload Resume</button>
        </form>        
    );
}

export default UploadForm;