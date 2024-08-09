import React, { useState } from 'react';
import axios from 'axios';
import styled from 'styled-components';

const FileUploaderContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border: 2px dashed ${props => props.theme.borderColor};
  border-radius: 10px;
  margin-bottom: 20px;
`;

const FileInput = styled.input`
  display: none;
`;

const UploadButton = styled.button`
  background-color: ${props => props.theme.primaryColor};
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 10px;
`;

const ResultContainer = styled.div`
  margin-top: 20px;
  width: 100%;
`;

const FileUploader = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Lütfen bir dosya seçin.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/upload-file/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setResult(response.data);
    } catch (error) {
      console.error('Dosya yükleme hatası:', error);
      alert('Dosya yüklenirken bir hata oluştu.');
    }
  };

  return (
    <FileUploaderContainer>
      <FileInput type="file" onChange={handleFileChange} id="file-input" />
      <UploadButton onClick={() => document.getElementById('file-input').click()}>
        Dosya Seç
      </UploadButton>
      {file && <p>{file.name}</p>}
      <UploadButton onClick={handleUpload}>Yükle ve Analiz Et</UploadButton>
      {result && (
        <ResultContainer>
          <h3>Analiz Sonuçları:</h3>
          <p>Metin: {result.text.substring(0, 100)}...</p>
          <h4>Varlık Listesi:</h4>
          <ul>
            {result.entity_list.map((entity, index) => (
              <li key={index}>{entity}</li>
            ))}
          </ul>
          <h4>Duygu Analizi Sonuçları:</h4>
          <ul>
            {result.results.map((item, index) => (
              <li key={index}>
                {item.entity}: {item.sentiment}
              </li>
            ))}
          </ul>
        </ResultContainer>
      )}
    </FileUploaderContainer>
  );
};

export default FileUploader;