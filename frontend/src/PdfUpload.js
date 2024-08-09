// PDFUploader.js
import React, { useState } from 'react';

const PdfUpload = () => {
    const [file, setFile] = useState(null);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        const formData = new FormData();
        formData.append('pdfFile', file);

        try {
            const response = await fetch('https://your-api-endpoint.com/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            console.log('Başarılı:', data);
        } catch (error) {
            console.error('Hata:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="file" accept="application/pdf" onChange={handleFileChange} />
            <button type="submit">Yükle</button>
        </form>
    );
};

export default PdfUpload;
